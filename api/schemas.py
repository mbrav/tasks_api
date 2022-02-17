from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None


class Status(BaseModel):
    message: str


class SignupIn(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    class_id: Optional[str] = None

    class Config:
        orm_mode = True


class SignupOut(SignupIn):
    created_at: datetime
    user_id: Optional[int] = None
