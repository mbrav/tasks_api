from datetime import datetime

from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.sql import func

from .db import Base


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True, index=True)
    result = Column(String)
    date_created = Column(
        String, default=datetime.utcnow().isoformat())
