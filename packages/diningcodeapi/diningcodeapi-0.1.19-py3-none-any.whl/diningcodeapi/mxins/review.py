import requests
from bs4 import BeautifulSoup

from diningcodeapi.config import HEADERS, API_VERSION_V1
from diningcodeapi.utils import parse_background_image_url_in_style, convert_css_width_percentage_to_star_point


class ReviewMixin:
    def get_reviews(self, store_code: str, page_no: int, page_size: int = 5, proxies=None):
        if page_no == 1:
            soup = self._request_first_page(store_code, proxies)
        else:
            soup = self._request_more_than_second_page(store_code, page_no, page_size, proxies)

        review_tags = soup.find_all("div", class_="latter-graph")
        reviews = []
        for review_tag in review_tags:
            review = self._parse_review(review_tag)
            reviews.append(review)

        return reviews


    def _parse_review(self, review_tag_soup):
        id = review_tag_soup.attrs['id']

        # 사용자 아바타 이미지 URL 획득
        avatar_container_tag = review_tag_soup.find_all("div")[0]
        avatar_tag = avatar_container_tag.find("div")
        avatar_url = parse_background_image_url_in_style(avatar_tag.attrs['style'])
        # 사용자 계정 별칭 획득
        person_grade_tag = review_tag_soup.find("p", class_="person-grade")
        nickname = person_grade_tag.find("strong").get_text()
        bio = person_grade_tag.find("span", class_="stxt").get_text()
        is_special_list = False
        badge_tag = person_grade_tag.find("img")
        if badge_tag:
            badge_url = badge_tag.attrs['src']
            if badge_url == 'https://s3-ap-northeast-1.amazonaws.com/dcicons/members/de3d409367e9c0da1f45827928bba8ea.png':
                is_special_list = True
        star_container_tag = review_tag_soup.find("span", class_="star-date")
        star_tag = star_container_tag.find("i", class_="star").contents[0]
        star_point = convert_css_width_percentage_to_star_point(star_tag.attrs['style'])
        date = star_container_tag.find("i", class_="date").get_text()

        # 상세 별점 획득

        # 리뷰 글 획득득
        content = review_tag_soup.find("p", class_="review_contents").get_text()

        # 맛집 평가 사진 획득득
        image_tags = review_tag_soup.find("div", class_="btn-gallery-review")
        review_image_urls = []
        for image_tag in image_tags:
            image_url = image_tag.attrs['src']
            review_image_urls.append(image_url)

        # 키워드 획득득
        tag_container_tag = review_tag_soup.find("p", class_="tags")
        tag_tags = tag_container_tag.find_all("span")
        tags = []
        for tag_tag in tag_tags:
            tag = tag_tag.get_text()
            tags.append(tag)

        # 공감 정보 획득
        num_symps = review_tag_soup.find("div", class_="symp-btn").get_text()

        result = {
            "_id": id,
            "id":id,
            "nickname": nickname,
            "bio": bio,
            "avatar": avatar_url,
            "star": {
                "point": star_point,
                "date": date
            },
            "is_special_list": is_special_list,
            "date": date,
            "content": content,
            "review_images": review_image_urls,
            "tags": tags,
            "num_symps": num_symps,
            "api-version":API_VERSION_V1,
        }

        return result

    def _request_first_page(self, store_code, proxies=None):
        response = requests.post(f'https://www.diningcode.com/profile.php?rid={store_code}', headers=HEADERS, proxies=proxies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        container_tag = soup.find('div', id='div_review')
        return container_tag

    def _request_more_than_second_page(self, store_code, page_no, page_size, proxies=None):
        url = f"https://www.diningcode.com/2018/ajax/review.php"
        data = {
            "mode": "LIST",
            "type": "profile",
            "v_rid": store_code,
            "page": page_no,
            "rows": page_size

        }
        response = requests.post(url, data=data, headers=HEADERS, proxies=proxies)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

