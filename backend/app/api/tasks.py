from typing import Optional

from app import db, models, schemas
from fastapi import APIRouter, Depends, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import (FilterQuery, SortByDescQuery, SortByQuery,
                   get_active_superuser, get_active_user)

router = APIRouter()


@router.post(
    path='',
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED)
async def task_post(
    schema: schemas.TaskIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database)
) -> models.Task:
    """Create new task with POST request"""

    new_object = models.Task(**schema.dict())
    return await new_object.save(db_session)


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TaskOut)
async def task_get(
    id: int,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Retrieve task with GET request"""

    get_object = await models.Task.get(db_session, id=id)
    return get_object


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def task_delete(
    id: int,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Retrieve task with GET request"""

    get_object = await models.Task.get(db_session, id=id)
    return await get_object.delete(db_session)


@router.patch(
    path='/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.TaskOut)
async def task_patch(
    id: int,
    schema: schemas.TaskIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Modify task with PATCH request"""

    get_object = await models.Task.get(db_session, id=id)
    return await get_object.update(db_session, **schema.dict())


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.TaskOut])
async def tasks_list(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    first_name: Optional[str] = FilterQuery,
    last_name: Optional[str] = FilterQuery,
    phone: Optional[str] = FilterQuery,
    email: Optional[str] = FilterQuery,
    class_id: Optional[str] = FilterQuery,
    user_id: Optional[int] = FilterQuery
):
    """List tasks with GET request"""

    return await models.Task.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        class_id=class_id,
        user_id=user_id,
    )

add_pagination(router)
