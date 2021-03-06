from datetime import datetime

from fastapi import HTTPException, status
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import Column, DateTime, Integer, inspect, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import text

Base = declarative_base()


def to_snake_case(str: str) -> str:
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c.lower())
        else:
            res.append(c)
    return ''.join(res)


class BaseModel(Base):
    """Abstract base model"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)

    @declared_attr
    def __tablename__(self) -> str:
        return to_snake_case(self.__name__) + 's'

    async def _update_modified(self):
        """Update time of object when modified"""
        self.updated_at = datetime.now()

    async def save(self, db_session: AsyncSession):
        """Save object

        Args:
            db_session (AsyncSession): Current db session

        Raises:
            HTTPException: Raise SQLAlchemy error
        """
        try:
            db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self)
            return self
        except IntegrityError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex.orig))
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    @classmethod
    async def get(
        self,
        db_session: AsyncSession,
        db_query: select = None,
        raise_404: bool = True,
        **kwarg
    ):
        """Get object based on query or id identified by kwarg

        Args:
            db_session (AsyncSession): Current db session
            query (select, optional): SQLAlchemy 2.0 select query. Defaults to None.
            raise_404 (bool, optional): Raise 404 if not found. Defaults to True.
            kwarg (optional): Object attribute and value by which
                to get object. Defaults to None.

        Raises:
            HTTPException: Raise SQLAlchemy error

        Returns:
            Database model or None
        """

        if not db_query:
            if not len(kwarg):
                db_query = select(self)
            else:
                key, value = next(iter(kwarg.items()))
                db_query = select(self).where(getattr(self, key) == value)

        try:
            result = await db_session.execute(db_query)
            obj = result.scalars().first()
            if obj or not raise_404:
                # Returns Null or object
                return obj
            detail = ''
            if len(kwarg):
                key, value = next(iter(kwarg.items()))
                detail = f'{self.__name__} with {key} = {value} not found'
            else:
                detail = f'{self.__name__} not found'
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail)

        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    async def update(self, db_session: AsyncSession, **kwargs):
        """Update model object with provided attributes"""

        for k, v in kwargs.items():
            setattr(self, k, v)
        try:
            await self._update_modified()
            db_session.add(self)
            await db_session.commit()
            return self
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    async def delete(self, db_session: AsyncSession):
        """Delete model object from database"""

        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    @classmethod
    async def _get_objects(
        self,
        db_session: AsyncSession,
        db_query: select = None,
        sort_by: str = None,
        desc: bool = True,
        paginated: bool = False,
        **kwargs
    ):
        """Get list of objects of paginated

        Args:
            db_session (AsyncSession): Current db session
            db_query (select, optional): SQLAlchemy 2.0 select query. Defaults to None.
            sort_by (str, optional): column by which to sort results.
            desc (bool, optional): Sort by descending. Defaults to True.

        Raises:
            HTTPException: Raise SQLAlchemy error

        Returns:
            paginate: fastapi_pagination result
            or
            Database models or None
        """

        filter_by = {k: v for k, v in kwargs.items() if v is not None}

        if not sort_by:
            sort_by = inspect(self).primary_key[0].name
        if db_query is None:
            column = self.__table__.columns.get(sort_by).name
            sort = 'desc'
            if not desc:
                sort = 'asc'
            if len(filter_by):
                db_query = select(self).order_by(
                    text(f'{column} {sort}')).filter_by(**filter_by)
            else:
                db_query = select(self).order_by(text(f'{column} {sort}'))

        try:
            if paginated:
                return await paginate(db_session, db_query)
            return await db_session.execute(db_query)
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    @classmethod
    async def get_list(self, db_session: AsyncSession, **kwargs) -> paginate:
        """Get list of objects"""
        return await self._get_objects(db_session, paginated=False, **kwargs)

    @classmethod
    async def paginate(self, db_session: AsyncSession, **kwargs) -> paginate:
        """Get paginated list of objects"""
        return await self._get_objects(db_session, paginated=True, **kwargs)
