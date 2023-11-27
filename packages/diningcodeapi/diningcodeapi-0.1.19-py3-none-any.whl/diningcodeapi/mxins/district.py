from sphinx.util import requests
import requests
from diningcodeapi.config import HEADERS, API_VERSION_V1


class DistrictMixin:
    def get_district(self, proxies=None):
        url = f"https://im.diningcode.com/API/recommend/"
        data = {
            "mode": "district"
        }
        response = requests.post(url, data=data, headers=HEADERS, proxies=proxies)
        response.raise_for_status()
        themes = response.json()
        themes['_id'] = 1
        themes['api-version'] = API_VERSION_V1
        return themes
