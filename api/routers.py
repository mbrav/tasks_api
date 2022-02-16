from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .db import get_db

router = APIRouter()


@router.get('/', tags=['index'])
async def index(message: str = None):
    """Index Function

    Args:
        message: Message to the server

    Returns:
        message: Message to the server
        response: Message from the server
        time: Server Time

    """

    response = {
        'message': f'{message}',
        'response': 'Fast API service for signups and Telegram integration',
        'time': datetime.utcnow().isoformat()
    }
    return response


@router.post('/signup', status_code=201, tags=['signups'])
async def signup_post(schema: schemas.Signup, db: Session = Depends(get_db)):
    """Generate new signup with POST request"""

    async def create():
        new_object = models.Signup(**schema.dict())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        return new_object

    response = await create()
    return response


@router.get('/signup/{id}', status_code=200, tags=['signups'])
async def signup_get(id: int, response: Response, db: Session = Depends(get_db)):
    """Retrieve result object with GET request"""

    result = db.query(models.Signup).filter(models.Signup.id == id).first()
    if not result:
        detail = f'Signup with id {id} was not found'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return result
