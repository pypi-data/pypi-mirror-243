from typing import Optional

from pydantic import BaseModel

from connector_vk_private_lib.src.interfaces.attachments import Attachment
from connector_vk_private_lib.src.interfaces.main import Repost, Error


class GetWallItemComment(BaseModel):
    can_post: int
    count: int
    groups_can_post: Optional[bool] = False


class GetWallItemLike(BaseModel):
    can_like: int
    count: int
    user_likes: int
    can_publish: int
    repost_disabled: bool


class GetWallPostSource(BaseModel):
    type: str


class GetWallPostTarget(BaseModel):
    name: str
    track_code: str


class GetWallPostSharing(BaseModel):
    targets: Optional[list[GetWallPostTarget]] = None


class GetWallItem(BaseModel):
    inner_type: str
    is_pinned: Optional[int] = None
    comments: Optional[GetWallItemComment] = None
    marked_as_ads: Optional[int] = None
    hash: str
    type: str
    attachments: Optional[list[Attachment]] = None
    date: int
    from_id: int
    id: int
    is_favorite: bool
    likes: Optional[GetWallItemLike] = None
    owner_id: int
    post_source: Optional[GetWallPostSource] = None
    post_type: str
    reposts: Optional[Repost] = None
    text: str
    sharing: Optional[GetWallPostSharing] = None
    next_from: Optional[str] = None


class ResponseGetWall200(BaseModel):
    count: int
    items: Optional[list[GetWallItem]] = None


class ResponseGetWall(BaseModel):
    response: Optional[ResponseGetWall200] = None
    error: Optional[Error] = None
