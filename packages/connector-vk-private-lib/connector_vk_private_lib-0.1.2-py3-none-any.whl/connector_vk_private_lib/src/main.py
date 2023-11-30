import os
import sys

root_path = os.getcwd()
sys.path.append(root_path)

from connector_vk_private_lib.src.config.main import VK_ACCESS_TOKEN, VK_GROUP_OWNER_ID, VK_GROUP_DONORS, \
    VK_FRIEND_GROUP, OWNER_ID, \
    POST_ON_BEHALF_OF_GROUP, TIMER, CURRENCY, COMMENT_REGEX, VK_METHOD_ENDPOINT, VK_WALL_GET_COMMENTS_METHOD, \
    VK_WALL_GET, VK_VIDEO_GET, VK_MESSAGE_SEND, VK_USER_GET, VK_WALL_POST_METHOD, VK_API_VERSION, VK_GROUPS_GET_METHOD
from connector_vk_private_lib.src.interfaces.main import BaseConfig
from connector_vk_private_lib.src.service.main import Connector


def init_connector() -> Connector or Exception:
    try:
        config = BaseConfig(
            VK_ACCESS_TOKEN=VK_ACCESS_TOKEN,
            VK_GROUP_OWNER_ID=VK_GROUP_OWNER_ID,
            VK_GROUP_DONORS=VK_GROUP_DONORS,
            VK_FRIEND_GROUP=VK_FRIEND_GROUP,
            OWNER_ID=OWNER_ID,
            POST_ON_BEHALF_OF_GROUP=POST_ON_BEHALF_OF_GROUP,
            TIMER=TIMER,
            CURRENCY=CURRENCY,
            COMMENT_REGEX=COMMENT_REGEX,
            VK_METHOD_ENDPOINT=VK_METHOD_ENDPOINT,
            VK_WALL_GET_COMMENTS_METHOD=VK_WALL_GET_COMMENTS_METHOD,
            VK_WALL_GET=VK_WALL_GET,
            VK_VIDEO_GET=VK_VIDEO_GET,
            VK_MESSAGE_SEND=VK_MESSAGE_SEND,
            VK_USER_GET=VK_USER_GET,
            VK_WALL_POST_METHOD=VK_WALL_POST_METHOD,
            VK_API_VERSION=VK_API_VERSION,
            VK_GROUPS_GET_METHOD=VK_GROUPS_GET_METHOD
        )

        return Connector(config)
    except Exception as e:
        return e


def init(
        _config: BaseConfig
) -> Connector or Exception:
    try:
        return Connector(_config)
    except Exception as e:
        return e
