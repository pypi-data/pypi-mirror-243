from typing import Optional

from pydantic import BaseModel


class AdsParams(BaseModel):
    vk_id: int
    duration: int
    video_id: str
    pl: int
    content_id: str
    sign: str
    groupId: Optional[int] = None
    vk_catid: int
    vk_content_mark_ids: Optional[list[int]] = []


class Ads(BaseModel):
    slot_id: int
    timeout: float
    can_play: int
    params: AdsParams
    sections: list[str]
    midroll_percents: list[float]
