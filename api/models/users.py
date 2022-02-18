from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from . import Base


class User(Base):
    """User class"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    full_name = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=func.now())
