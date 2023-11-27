import logging

__VERSION__ = "0.1.19"

from diningcodeapi.mxins.blog import BlogMixin
from diningcodeapi.mxins.district import DistrictMixin
from diningcodeapi.mxins.review import ReviewMixin
from diningcodeapi.mxins.store import StoreMixin
from diningcodeapi.mxins.theme import ThemeMixin

DEFAULT_LOGGER = logging.getLogger("diningcodeapi")


class Client(

    StoreMixin,
    DistrictMixin,
    ThemeMixin,
    BlogMixin,
    ReviewMixin,

):
    pass
