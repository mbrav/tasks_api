from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    """User class"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    full_name = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=func.now())


class Signup(Base):
    """Signup class"""

    __tablename__ = 'signups'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey(User.id),
        nullable=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String(30), nullable=False)
    class_id = Column(String(60), nullable=True)
    created_at = Column(DateTime, default=func.now())
