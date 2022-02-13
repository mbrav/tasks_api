from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .db import get_db
from .models import Result
from .utils import Random

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
        'response': 'Fast API random number generator',
        'time': datetime.utcnow().isoformat()
    }
    return response


@router.post('/generate', status_code=201, tags=['random'])
async def generate(db: Session = Depends(get_db)):
    """Generate new result object with POST request"""

    async def create():
        rand = Random.rand_int()
        new_result = Result(
            result=str(rand))
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        return new_result

    response = await create()
    return response


@router.get('/retrieve/{id}', status_code=200, tags=['random'])
async def retrieve(id: int, response: Response, db: Session = Depends(get_db)):
    """Retrieve result object with GET request"""

    result = db.query(Result).filter(Result.id == id).first()
    if not result:
        detail = f'Result with id {id} was not found'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return result
