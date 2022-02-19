from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from ..db import Base


class User(Base):
    """User class"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    password = Column(String(128), nullable=True)
    email = Column(String(30), nullable=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    created_at = Column(DateTime, default=func.now())

    def __init__(self, username, password):
        self.start = username
        self.end = password