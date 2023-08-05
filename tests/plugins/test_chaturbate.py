from streamlink.plugins.chaturbate import Chaturbate
from tests.plugins import PluginCanHandleUrl


class TestPluginCanHandleUrlChaturbate(PluginCanHandleUrl):
    __plugin__ = Chaturbate

    should_match = [
        "https://www.chaturbate.com/babbysonfiree",
        "http://www.chaturbate.com/babbysonfiree",
        "https://chaturbate.com/babbysonfiree",
        "http://chaturbate.com/babbysonfiree",
    ]

    should_not_match = [
        "https://www.chaturbate.com",
    ]
