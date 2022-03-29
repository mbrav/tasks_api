from datetime import datetime, timedelta

from app.schemas import TaskStatus
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, PickleType,
                        String, Text, and_, or_, select)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from .base import BaseModel
from .users import User


class Task(BaseModel):
    """Task class"""

    name = Column(String(40), nullable=False)
    qwargs = Column(PickleType, nullable=False)
    result = Column(Text, nullable=True)
    status = Column(String(20), nullable=False)
    delay_seconds = Column(Integer, nullable=False)

    planned_for = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='tasks')

    def __init__(self,
                 user_id: int,
                 qwargs: str,
                 name: str,
                 delay_seconds: int = 0,
                 planned_for: datetime = None,
                 completed_at: datetime = None,
                 status: str = 'created',
                 result: str = None):
        self.user_id = user_id
        self.qwargs = qwargs
        self.name = name
        self.delay_seconds = delay_seconds
        self.completed_at = completed_at
        self.status = status
        self.result = result
        self.planned_for = datetime.now() + timedelta(seconds=delay_seconds)

    async def _update_modified(self):
        """Update time of object when modified"""
        self.updated_at = datetime.now()
        if not self.result:
            if self.planned_for < datetime.now():
                self.status = TaskStatus.expired
                self.completed_at = None
            elif self.status != TaskStatus.rescheduled:
                self.status = TaskStatus.created

    async def add_result(self, result_text: str):
        """Update model with result"""
        await self._update_modified()
        self.completed_at = datetime.now()
        self.result = result_text
        self.status = TaskStatus.completed

    async def update_planned_for(self, seconds: int):
        """Update planned for time when delay is modified"""
        self.status = TaskStatus.rescheduled
        self.delay_seconds = seconds
        self.planned_for = self.created_at + timedelta(seconds=seconds)
        await self._update_modified()

    @classmethod
    async def get_executable_tasks(self, db_session: AsyncSession):
        """Get available tasks for execution"""
        db_query = select(self).where(and_(
            or_(self.status == TaskStatus.created,
                self.status == TaskStatus.rescheduled),
            self.planned_for > datetime.now(),
        )).order_by(
            self.created_at.asc())
        tasks = await self.get_list(db_session, db_query=db_query)
        return tasks

    @classmethod
    async def get_expired_tasks(self, db_session: AsyncSession):
        """Get expired tasks"""
        db_query = select(self).where(and_(
            self.status == TaskStatus.expired,
        )).order_by(
            self.created_at.asc())
        tasks = await self.get_list(db_session, db_query=db_query)
        return tasks
