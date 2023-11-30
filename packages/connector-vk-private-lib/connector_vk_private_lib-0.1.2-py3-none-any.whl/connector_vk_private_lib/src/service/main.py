import requests
import os
import sys
from urllib.parse import urlencode

root_path = os.getcwd()
sys.path.append(root_path)

from connector_vk_private_lib.src.interfaces.main import BaseConfig, \
    URLQueryPost, \
    URLQueryUserInfo, \
    URLQueryMessageSend, \
    URLQueryWallGet, \
    URLQueryVideoGet, \
    URLQueryCommentsGet, \
    URLQueryGroupGet
from connector_vk_private_lib.src.interfaces.groups import ResponseGetGroups
from connector_vk_private_lib.src.interfaces.wall import ResponseGetWall
from connector_vk_private_lib.src.interfaces.video import ResponseGetVideo


class Connector:
    config: BaseConfig

    def __init__(self, _config: BaseConfig):
        self.config = _config

    @staticmethod
    def build_url(
            origin: str,
            query: dict
    ):
        return origin + urlencode(query)

    def build_post_url(
            self,
            message: str,
            attachments: list[str]
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_WALL_POST_METHOD

        _query: URLQueryPost = URLQueryPost(
            access_token=self.config.VK_ACCESS_TOKEN,
            owner_id=self.config.OWNER_ID,
            from_group=self.config.POST_ON_BEHALF_OF_GROUP,
            message=message,
            attachments=attachments,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_user_info_url(
            self,
            _name: str,
            _user_ids: list[int]
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_USER_GET

        _query: URLQueryUserInfo = URLQueryUserInfo(
            access_token=self.config.VK_ACCESS_TOKEN,
            user_ids=_user_ids,
            name_case=_name,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_message_send_url(
            self,
            _user_id: int,
            _random_id: str,
            _message: str,
            _attachments: list[str]
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_MESSAGE_SEND

        _query: URLQueryMessageSend = URLQueryMessageSend(
            access_token=self.config.VK_ACCESS_TOKEN,
            user_id=_user_id,
            random_id=_random_id,
            message=_message,
            attachments=_attachments,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_video_get_url(
            self,
            _video_owner_id: int,
            _videos: str,
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_VIDEO_GET

        _query: URLQueryVideoGet = URLQueryVideoGet(
            access_token=self.config.VK_ACCESS_TOKEN,
            owner_id=_video_owner_id,
            count=1,
            v=self.config.VK_API_VERSION,
            videos=_videos,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_groups_get_url(
            self,
            _filter: str
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_GROUPS_GET_METHOD

        _query: URLQueryGroupGet = URLQueryGroupGet(
            access_token=self.config.VK_ACCESS_TOKEN,
            owner_id=self.config.OWNER_ID,
            filter=_filter,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_wall_get_url(
            self,
            _owner_id: int,
            _amount: int
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_WALL_GET

        _query: URLQueryWallGet = URLQueryWallGet(
            access_token=self.config.VK_ACCESS_TOKEN,
            owner_id=_owner_id,
            count=_amount,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def build_comments_get_url(
            self,
            _post_id: int,
    ):
        _origin = self.config.VK_METHOD_ENDPOINT + self.config.VK_WALL_POST_METHOD

        _query: URLQueryCommentsGet = URLQueryCommentsGet(
            access_token=self.config.VK_ACCESS_TOKEN,
            owner_id=self.config.OWNER_ID,
            post_id=_post_id,
            count=100,
            v=self.config.VK_API_VERSION,
        )

        return self.build_url(_origin, _query.__dict__)

    def get_post(
            self,
            message: str,
            attachments: list[str]
    ):
        _url = self.build_post_url(message, attachments)
        _res = requests.get(_url)

        return _res.json()["response"]

    def send_message(
            self,
            _user_id: int,
            _random_id: str,
            message: str,
            attachments: list[str] = ""
    ):
        _url = self.build_message_send_url(
            _user_id,
            _random_id,
            message,
            attachments
        )
        _res = requests.get(_url)

        return _res.json()["response"]

    def user_info(
            self,
            _name: str,
            _user_ids: list[int],
    ):
        _url = self.build_user_info_url(
            _name,
            _user_ids,
        )
        _res = requests.get(_url)

        return _res.json()["response"]

    def get_comments(
            self,
            _post_id: int
    ):
        _url = self.build_comments_get_url(
            _post_id
        )
        _res = requests.get(_url)

        return _res.json()["response"]

    def get_wall(
            self,
            _owner_id: int,
            _amount: int = 30
    ):
        _url = self.build_wall_get_url(
            _owner_id,
            _amount
        )
        _response_json = requests.get(_url).json()

        return ResponseGetWall(**_response_json)

    def get_video(
            self,
            _video_owner_id: int,
            _videos: str
    ):
        _url = self.build_video_get_url(
            _video_owner_id,
            _videos
        )
        _res = requests.get(_url).json()

        return ResponseGetVideo(**_res)

    def get_groups(
            self,
            _filter: str = ""
    ):
        _url = self.build_groups_get_url(
            _filter
        )
        _response_json = requests.get(
            _url
        ).json()

        return ResponseGetGroups(**_response_json)
