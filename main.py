from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from api import models, schemas
from api.db import SessionLocal, engine
from api.utils import Random

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/', tags=['index'])
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


@app.post('/generate', status_code=201, tags=['random'])
async def generate(db: Session = Depends(get_db)):
    """Generate new result object with POST request"""

    async def create():
        rand = Random.rand_int()
        new_result = models.Result(
            result=str(rand))
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        return new_result

    response = await create()
    return response


@app.get('/retrieve/{id}', status_code=200, tags=['random'])
async def retrieve(id: int, response: Response, db: Session = Depends(get_db)):
    """Retrieve result object with GET request"""

    result = db.query(models.Result).filter(models.Result.id == id).first()
    if not result:
        detail = f'Result with id {id} was not found'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return result


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
