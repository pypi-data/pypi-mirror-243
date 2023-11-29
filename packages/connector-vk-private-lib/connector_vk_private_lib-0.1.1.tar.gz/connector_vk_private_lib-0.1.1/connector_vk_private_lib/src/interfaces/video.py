from typing import Optional

from pydantic import BaseModel

from connector_vk_private_lib.src.interfaces.ads import Ads
from connector_vk_private_lib.src.interfaces.main import Error, Like, Repost
from connector_vk_private_lib.src.interfaces.photo import Image


class Video(BaseModel):
    response_type: str
    access_key: Optional[str] = None
    can_comment: Optional[int] = None
    can_like: Optional[int] = None
    can_repost: Optional[int] = None
    can_subscribe: Optional[int] = None
    can_add_to_faves: Optional[int] = None
    can_add: Optional[int] = None
    comments: Optional[int] = None
    date: Optional[int] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    image: Optional[list[Image]] = None
    first_frame: Optional[list[Image]] = []
    width: Optional[int] = None
    height: Optional[int] = None
    id: Optional[int] = None
    owner_id: Optional[int] = None
    title: Optional[str] = None
    is_favorite: Optional[bool] = None
    track_code: Optional[str] = None
    type: Optional[str] = None
    views: Optional[int] = None
    local_views: Optional[int] = None
    can_dislike: Optional[int] = None


class VideoTimelineThumbs(BaseModel):
    count_per_image: int
    count_per_row: int
    count_total: int
    frame_height: int
    frame_width: float
    links: list[str]
    is_uv: bool
    frequency: int


class ResponseGetVideoItem(BaseModel):
    files: Optional[dict] = None
    trailer: Optional[dict] = None
    timeline_thumbs: Optional[VideoTimelineThumbs] = None
    ads: Optional[Ads] = None
    response_type: Optional[str] = None
    access_key: Optional[str] = None
    can_comment: Optional[int] = None
    can_like: Optional[int] = None
    can_repost: Optional[int] = None
    can_subscribe: Optional[int] = None
    can_add_to_faves: Optional[int] = None
    can_add: Optional[int] = None
    can_play_in_background: Optional[int] = None
    can_download: Optional[int] = None
    comments: Optional[int] = None
    date: Optional[int] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    image: Optional[list[Image]] = None
    width: Optional[int] = None
    height: Optional[int] = None
    id: Optional[int] = None
    owner_id: Optional[int] = None
    ov_id: Optional[str] = None
    title: Optional[str] = None
    is_favorite: Optional[bool] = None
    player: Optional[str] = None
    added: Optional[int] = None
    repeat: Optional[int] = None
    type: Optional[str] = None
    views: Optional[int] = None
    local_views: Optional[int] = None
    likes: Optional[Like] = None
    reposts: Optional[Repost] = None
    can_dislike: Optional[int] = None


class ResponseGetVideo200(BaseModel):
    count: int
    items: list[ResponseGetVideoItem]


class ResponseGetVideo(BaseModel):
    response: Optional[ResponseGetVideo200] = None
    error: Optional[Error] = None
