from fastapi import APIRouter

from . import auth, index, tasks, users

api_router = APIRouter()
api_router.include_router(index.router, tags=['Index'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(tasks.router, prefix='/tasks', tags=['Tasks'])
