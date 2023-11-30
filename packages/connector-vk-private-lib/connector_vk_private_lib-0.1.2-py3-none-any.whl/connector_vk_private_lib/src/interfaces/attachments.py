from typing import Optional

from pydantic import BaseModel

from connector_vk_private_lib.src.interfaces.photo import Photo
from connector_vk_private_lib.src.interfaces.video import Video


class Attachment(BaseModel):
    type: str
    photo: Optional[Photo] = None
    video: Optional[Video] = None
    text: Optional[str] = None
    user_id: Optional[int] = None
    owner_id: Optional[int] = None
    web_view_token: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None


class RequestAttachments(BaseModel):
    data: list[Attachment]
