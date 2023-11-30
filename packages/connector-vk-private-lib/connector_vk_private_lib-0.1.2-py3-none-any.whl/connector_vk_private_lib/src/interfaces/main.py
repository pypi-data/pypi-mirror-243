from typing import Optional
from pydantic import BaseModel


class BaseConfig(BaseModel):
    VK_ACCESS_TOKEN: str
    VK_GROUP_OWNER_ID: int
    VK_GROUP_DONORS: list[str]
    VK_FRIEND_GROUP: int
    OWNER_ID: int
    POST_ON_BEHALF_OF_GROUP: str
    TIMER: int
    CURRENCY: int
    COMMENT_REGEX: str
    VK_METHOD_ENDPOINT: str
    VK_WALL_GET_COMMENTS_METHOD: str
    VK_WALL_GET: str
    VK_VIDEO_GET: str
    VK_MESSAGE_SEND: str
    VK_USER_GET: str
    VK_WALL_POST_METHOD: str
    VK_API_VERSION: str
    VK_GROUPS_GET_METHOD: str


class URLQueryPost(BaseModel):
    access_token: str
    owner_id: int
    from_group: int
    message: str
    attachments: list[str]
    v: str


class URLQueryUserInfo(BaseModel):
    access_token: str
    user_ids: list[int]
    name_case: str
    v: str


class URLQueryMessageSend(BaseModel):
    access_token: str
    user_id: int
    random_id: str
    message: str
    attachments: list[str]
    v: str


class URLQueryVideoGet(BaseModel):
    access_token: str
    videos: str
    owner_id: int
    count: int
    v: str


class URLQueryWallGet(BaseModel):
    access_token: str
    owner_id: int
    count: int
    v: str


class URLQueryGroupGet(BaseModel):
    access_token: str
    owner_id: int
    filter: str
    v: str


class URLQueryCommentsGet(BaseModel):
    access_token: str
    owner_id: int
    post_id: int
    count: int
    v: str


class RequestParam(BaseModel):
    key: str
    value: str


class Error(BaseModel):
    error_code: int
    error_msg: str
    request_params: Optional[list[RequestParam]] = None


class Like(BaseModel):
    count: int
    user_likes: int


class Repost(BaseModel):
    count: int
