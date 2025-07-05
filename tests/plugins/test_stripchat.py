from streamlink.plugins.stripchat import Stripchat
from tests.plugins import PluginCanHandleUrl


class TestPluginCanHandleUrlStripchat(PluginCanHandleUrl):
    __plugin__ = Stripchat

    should_match = [
        "https://www.stripchat.com/kategoodgirl",
        "http://www.stripchat.com/kategoodgirl",
        "https://www.stripchat.com/kategoodgirl",
        "http://www.stripchat.com/kategoodgirl",
    ]

    should_not_match = [
        "https://www.stripchat.com",
    ]
