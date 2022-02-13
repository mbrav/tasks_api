from typing import List, Optional

from pydantic import BaseModel


class Result(BaseModel):
    id: int
    result: str
    date_created: str
