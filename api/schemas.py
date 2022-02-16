from typing import List, Optional

from pydantic import BaseModel


class Signup(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    class_id: str
    date_created: str
