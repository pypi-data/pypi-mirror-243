from sphinx.util import requests
import requests
from diningcodeapi.config import HEADERS


class ThemeMixin:
    def get_themes(self, region: str, page_no: int, proxies=None):
        url = f"https://im.diningcode.com/API/recommend/"
        data = {
            "lat": "",
            "lng": "",
            "page": page_no,
            "region": region,
            "token": "",
            "session": {"type": "area", "area": "서울", "hour": 15},
            "mode": "home",
            "device": "web",
        }
        response = requests.post(url, data=data, headers=HEADERS, proxies=proxies)
        response.raise_for_status()
        themes = response.json()

        pass
        return themes
