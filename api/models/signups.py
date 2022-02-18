from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from . import Base
from .users import User


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
