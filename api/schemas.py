from typing import List, Optional

from pydantic import BaseModel


class SignupIn(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    class_id: str


class SignupOut(SignupIn):
    date_created: str


class SignupOut(BaseModel):
    data: List[SignupIn]
