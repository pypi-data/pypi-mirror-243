from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    login: str
    password: str
    code: Optional[str]
    verification_method: Optional[str]
