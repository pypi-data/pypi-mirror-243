from typing import Optional
from pydantic import BaseModel
from connector_vk_private_lib.src.interfaces.main import Error


class ResponseGetGroups200(BaseModel):
    count: int
    items: list[int]


class ResponseGetGroups(BaseModel):
    response: Optional[ResponseGetGroups200] = None
    error: Optional[Error] = None
