from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from .db import Base


class Signup(Base):
    __tablename__ = 'signups'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30))
    last_name = Column(String(30))
    phone = Column(String(12))
    email = Column(String(30))
    class_id = Column(String(60))
    date_created = Column(
        DateTime, default=func.now())
