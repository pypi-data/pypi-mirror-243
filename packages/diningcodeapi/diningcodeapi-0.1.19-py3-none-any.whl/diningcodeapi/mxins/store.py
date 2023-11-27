import requests
from bs4 import BeautifulSoup

from diningcodeapi.config import HEADERS, API_VERSION_V1
from diningcodeapi.utils import parse_bracketed_data, parse_number, parse_business_hour_pattern, \
    parse_date_and_day_of_the_week_pattern, is_special_business_hour, parse_special_business_hour, \
    parse_single_special_business_hour, is_single_special_business_hour, is_date_and_day_of_the_week_pattern, \
    is_special_day_without_time_pattern, parse_special_day_without_time_pattern

keyword_list = ['배달', '아침식사', '점심식사', '저녁식사', '식사모임', '술모임', '혼밥',
                '혼술', '회식', '데이트', '기념일', '가족외식', '간식', '숨은맛집',
                '서민적인', '캐주얼한', '고급스러운', '격식있는', '가성비좋은', '푸짐한',
                '조용한', '시끌벅적한', '예쁜', '깔끔한', '이국적/이색적',
                '경관/야경이좋은', '지역주민이찾는']
conv_list = ['무료주차', '발렛주차', '주차불가', '개별룸', '대형룸', '24시간영업', '야외좌석(테라스)', '놀이방', '애완동물동반', '콜키지무료']
purpose_list = ['아침식사', '점심식사', '저녁식사', '식사모임', '가족외식', '배달', '아이동반', '다이어트식당',
                '실버푸드', '술모임', '차모임', '혼카페', '혼밥', '혼술', '접대', '회식', '데이트', '기념일', '간식']


class StoreMixin:
    def get_stores(self, keyword: str, page_no: int, page_size: int = 20, proxies=None):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Origin': 'https://www.diningcode.com',
            "accept": "application/json, text/plain, */*",
            "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "sec-ch-ua": "\"Google Chrome\";v=\"119\", \"Chromium\";v=\"119\", \"Not?A_Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://www.diningcode.com/",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        data = {
            'query': keyword,
            'order': 'r_score',
            'rn_search_flag': 'on',
            'search_type': 'poi_search',
            'page': page_no,
            'size': page_size
        }
        response = requests.post('http://im.diningcode.com/API/isearch/',
                                 headers=headers,
                                 data=data,
                                 allow_redirects=False,
                                 proxies=proxies)
        response.raise_for_status()
        response_data = response.json()
        stores = response_data['result_data']['poi_section']['list']
        for store in stores:
            store['_id'] = store['v_rid']
            store['id'] = store['v_rid']
        return stores

    def _parse_address(self, address_container_soup):
        address = " ".join(map(lambda x: x.get_text(), address_container_soup.find_all("a")))
        lot_number = address_container_soup.find("span").get_text()
        address = f'{address} {lot_number}'
        return address

    def _parse_phone(self, phone_contaienr_soup):
        phone = phone_contaienr_soup.get_text()
        return phone

    def _parse_tag(self, tag_contaienr_soup):
        tag = tag_contaienr_soup.get_text()
        tags = tag.split(",")
        return tags

    def _parse_character(self, character_container_soup):
        characters_text = character_container_soup.get_text()
        characters = characters_text.split(",")
        return characters

    def _parse_business_hours(self, businessHours_container_soup):

        business_hour_tags = []
        business_hour_today_container = businessHours_container_soup.find("div", class_="busi-hours-today")
        business_hour_tags.extend(business_hour_today_container.find_all("p", class_="r-txt"))

        business_hour_others_container = businessHours_container_soup.find("div", class_="busi-hours")
        business_hour_tags.extend(business_hour_others_container.find_all("p", class_="r-txt"))

        business_hours = []
        for business_hour_tag in business_hour_tags:
            day_text = business_hour_tag.parent.get_text().strip()

            is_special_hour = is_special_business_hour(day_text)
            business_hour = {}
            if is_special_hour:
                day = parse_special_business_hour(day_text)
                business_hour['day'] = day
            is_single_special_hour = is_single_special_business_hour(day_text)
            if is_single_special_hour:
                day = parse_single_special_business_hour(day_text)
                business_hour['day'] = day
            is_date_and_day_of_the_week = is_date_and_day_of_the_week_pattern(day_text)

            if is_date_and_day_of_the_week:
                day = parse_date_and_day_of_the_week_pattern(day_text)
                hour_text = business_hour_tag.get_text().strip()
                is_special_day_without_time = is_special_day_without_time_pattern(hour_text)
                if not is_special_day_without_time:
                    hour = parse_business_hour_pattern(hour_text)
                else:
                    hour = None
                business_hour['day'] = day
                business_hour['hour'] = hour
            business_hours.append(business_hour)
            pass
        return business_hours

    def _parse_menu_info(self, menu_info_container_soup):
        menu_item_tags = menu_info_container_soup.find_all("li")
        menus = []
        for menu_item_tag in menu_item_tags:
            name = menu_item_tag.find("span", class_="Restaurant_Menu").get_text()
            price = menu_item_tag.find("p", class_="Restaurant_MenuPrice").get_text()
            menus.append({
                "name": name,
                "price": price
            })
        return menus

    def _parse_grade(self, grade_container_soup):
        score = grade_container_soup.find("strong").get_text()
        review_point_tag = grade_container_soup.find("span", class_="point")

        votes_text = review_point_tag.contents[0].strip()
        votes = parse_number(votes_text)
        review_point = review_point_tag.find("strong").get_text()

        return {"score": score, "review": {"review_point": review_point, "votes": votes}}

    def _parse_region(self, profile_container_soup):
        region_category_tag = profile_container_soup.find("div", class_="btxt")
        a_tags = region_category_tag.find_all("a")
        region = a_tags[0].get_text()
        return region

    def _parse_categories(self, profile_container_soup):
        region_category_tag = profile_container_soup.find("div", class_="btxt")
        a_tags = region_category_tag.find_all("a")
        categories = list(map(lambda x: x.get_text(), a_tags[1:]))
        return categories

    def _parse_likes(self, likes_container_soup):
        likes_text = likes_container_soup.find("span").get_text()
        parsed_data = parse_bracketed_data(likes_text)
        likes = parsed_data['value']
        return likes

    def _parse_banners(self, banner_container_tag_soup):
        banner_tags = banner_container_tag_soup.find_all("li")
        banner_urls = []
        for banner_tag in banner_tags:
            banner_url = banner_tag.find("img").attrs['src']
            banner_urls.append(banner_url)
        return banner_urls

    def _parse_evaluation_graph(self, evaluation_graph_tag_soup):
        evaluation_graph_tag = evaluation_graph_tag_soup.find("ul", class_='app-graph')
        evaluation_tags = evaluation_graph_tag.find_all("li")
        evaluations = []
        for evaluation_tag in evaluation_tags:
            evaluation_text = evaluation_tag.find("p", class_="btxt").get_text()
            parsed_data = parse_bracketed_data(evaluation_text)
            name = parsed_data['name']
            value = parsed_data['value']
            evaluations.append({"name": name, "value": value})
        return evaluations

    def _parse_start_point(self, graph_info_tag_soup):
        star_point_container_tag = graph_info_tag_soup.find("p", id="lbl_star_point")
        star_point_tag = star_point_container_tag.find("span", class_="point")
        point = star_point_tag.get_text()

        point_details = []
        point_detail_tag = graph_info_tag_soup.find("p", class_="point-detail")
        point_detail_item_tags = point_detail_tag.find_all("span")
        for point_detail_item_tag in point_detail_item_tags:
            name = point_detail_item_tag.get_text()
            point_tag = point_detail_item_tag.find("i")
            text = point_tag.get_text()

            point_details.append({"name": name, "point": text})
        result = {
            "point": point,
            "details": point_details
        }
        return result

    def _parse_tag_cloud_image(self, tag_cloud_image_tag_soup):
        img_tag = tag_cloud_image_tag_soup.find("img")
        img_url = img_tag.attrs['src']
        return img_url

    def _parse_keywords(self, graph_info_tag_soup):
        keyword_evaluation_tag_container = graph_info_tag_soup.find("ul", class_="app-arti")
        group_tags = keyword_evaluation_tag_container.find_all("li")

        groups = []
        for group_tag in group_tags:
            group_name = group_tag.find("span", class_="btxt").get_text()
            keywords = []
            keyword_tags = group_tag.find_all("span", class_="icon")
            for keyword_tag in keyword_tags:
                keyword_text = keyword_tag.get_text()
                keyword = parse_bracketed_data(keyword_text)
                keywords.append(keyword)

            groups.append({"group": group_name, "keywords": keywords})
        return groups

    def _parse_geo_cordinate(self, mini_map_tag_soup):
        latitude_tag = mini_map_tag_soup.find("input", id="hdn_lat")
        latitude = latitude_tag.attrs['value']
        longitude_tag = mini_map_tag_soup.find("input", id="hdn_lng")
        longitude = longitude_tag.attrs['value']
        return {
            "latitude": latitude,
            "longitude": longitude
        }

    def _parse_sufficient_reviews(self, warn_sav_tag_soup):
        tag = warn_sav_tag_soup.find("p", class_="btxt").get_text()
        if "신뢰" in tag:
            return True
        else:
            return False

    def get_banners(self, code: str, proxies = None):
        response = requests.get(f'https://www.diningcode.com/2018/ajax/gallery.php?rid={code}',
                                headers=HEADERS,
                                proxies=proxies
                                )
        soup = BeautifulSoup(response.text, 'html.parser')
        banner_container_tag_soup = soup.find("ul", class_="gallery-thumb-list")
        banner_urls = self._parse_banners(banner_container_tag_soup)

        return banner_urls

    def get_store(self, code: str, proxies = None):
        response = requests.post(f'https://www.diningcode.com/profile.php?rid={code}',
                                 headers=HEADERS,
                                 proxies=proxies
                                 )
        soup = BeautifulSoup(response.text, 'html.parser')
        store_name = soup.find('div', class_='tit-point').get_text().replace('\n', '')

        # 가게 기본 정보 획득
        basic_info = soup.find("div", class_="basic-info")
        info_items = basic_info.find_all('li')

        # 지역 정보 획득
        profile_container_soup = soup.find("div", id="div_profile")
        region = self._parse_region(profile_container_soup)
        categories = self._parse_categories(profile_container_soup)

        # 배너 이미지 정보 획득
        banner_urls = self.get_banners(code)

        # 카테고리 정보 획득

        # 좋아요 정보 획득
        likes_tag_container = soup.find("div", class_="favor-pic-appra")
        likes = self._parse_likes(likes_tag_container)

        # 점수 정보 획득
        grade_tag_container = soup.find("p", class_="grade")
        score = self._parse_grade(grade_tag_container)

        address = self._parse_address(info_items[0])
        phone = self._parse_phone(info_items[1])
        tags = self._parse_tag(info_items[2])
        characters = self._parse_character(info_items[3])

        # 영업시간 정보 획득 : 잠시 보류
        business_hour_container = soup.find("div", id="div_hour")
        business_hours = self._parse_business_hours(business_hour_container)
        # business_hours = self._parse_business_hours(business_hour_container)

        graph_info_tag_container = soup.find("div", class_="grade-info")
        evaluation_hist_data = self._parse_evaluation_graph(graph_info_tag_container)
        # 메뉴 정보 획득
        menu_tag_container = soup.find("div", class_="menu-info")
        menus = self._parse_menu_info(menu_tag_container)

        point = self._parse_start_point(graph_info_tag_container)
        keywords = self._parse_keywords(graph_info_tag_container)

        # 맛집 태그 클라우드 이미지 획득
        tag_cloud_tag_container = soup.find("div", class_="taste-tag")
        if tag_cloud_tag_container:
            cloud_img_url = self._parse_tag_cloud_image(tag_cloud_tag_container)
        else:
            cloud_img_url = ""
        # 가게 위도/경도 좌표 획득
        mini_map_tag_contaienr = soup.find("div", class_="mini-map")
        geo_coord = self._parse_geo_cordinate(mini_map_tag_contaienr)

        # 충분한 평가가 수행됬는지 여부를 나타내는 정보 획득
        warn_sav_tag_container = soup.find("div", class_="warn-sav")
        sufficient_reviews = self._parse_sufficient_reviews(warn_sav_tag_container)

        return {
            "_id": code,
            "id": code,
            "name": store_name,
            "region": region,
            "categories": categories,
            "banner_urls": banner_urls,
            "likes": likes,
            "score": score,
            "address": address,
            "phone": phone,
            "tags": tags,
            "characters": characters,
            "business_hours": business_hours,
            "evaluation_hist_data": evaluation_hist_data,
            "menus": menus,
            "point": point,
            "keywords": keywords,
            "cloud_img_url": cloud_img_url,
            "geo_coord": geo_coord,
            "sufficient_reviews": sufficient_reviews,
            "api-version": API_VERSION_V1,
        }