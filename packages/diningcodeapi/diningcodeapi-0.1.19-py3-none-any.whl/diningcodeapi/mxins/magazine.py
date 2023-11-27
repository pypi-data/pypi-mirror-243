import requests
from bs4 import BeautifulSoup

from diningcodeapi.config import HEADERS, API_VERSION_V1
from diningcodeapi.utils import parse_blog_id_from_query_parameter, is_days_ago, parse_days_ago, \
    calculate_date_from_days_ago, has_image_tag


class ManagzineMixin:

    def get_magazines(self, page_no, proxies=None):
        response = requests.post(f'https://www.diningcode.com/magazine.php?page={page_no}', headers=HEADERS,
                                 proxies={"http": proxies})
        soup = BeautifulSoup(response.text, 'html.parser')

        container_tag = soup.find("div", class_='board-list')
        item_tags = container_tag.find_all("li")

        magazines = []

        for item_tag in item_tags:
            link_tag = item_tag.find("a")
            link_query = link_tag.attrs['href']
            id = parse_blog_id_from_query_parameter(link_query)
            title = item_tag.find("h2", class_="title").get_text()
            description = item_tag.find("div", class_="preview").get_text()
            date_text = item_tag.find("div", class_="date").get_text()
            if is_days_ago(date_text):
                days_ago = parse_days_ago(date_text)
                date = calculate_date_from_days_ago(days_ago)
            else:
                date = date_text

            image_tag = item_tag.find("img")
            image_url = image_tag.attrs['src']
            thumbnail_url = image_url

            magazines.append({
                "id": id,
                "title": title,
                "date": date,
                "description": description,
                "url": thumbnail_url,
                "api-version": API_VERSION_V1,
            })

        return magazines

    def get_managzine(self, id: str, proxies=None):
        response = requests.post(f'https://www.diningcode.com/magazine.php?bid={id}', headers=HEADERS,
                                 proxies=proxies)
        soup = BeautifulSoup(response.text, 'html.parser')

        header_tag = soup.find("div", class_="board-header")
        title = header_tag.find("h2").get_text()
        date_text = header_tag.find("div", class_="date").get_text()
        if is_days_ago(date_text):
            days_ago = parse_days_ago(date_text)
            date = calculate_date_from_days_ago(days_ago)
        else:
            date = date_text

        container_tag = soup.find("div", class_='contents')
        content_tags = container_tag.find_all("p")
        contents = []
        for content_tag in content_tags:
            is_image_content = has_image_tag(content_tag)
            if is_image_content == True:
                image_url = content_tag.find("img").attrs['src']
                contents.append(image_url)
            else:
                text = content_tag.get_text()
                contents.append(text)

            # TODO: a 태그가 하나있을때, 복수개 있을때 추가 처리 필요

        result = {
            "_id": id,
            "title": title,
            "date": date,
            "contents": contents,
            "api-version": API_VERSION_V1
        }
        return result
