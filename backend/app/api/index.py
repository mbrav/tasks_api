from datetime import datetime

from fastapi import APIRouter

router = APIRouter()


@router.get('/', tags=['index'])
async def index(message: str = None):
    """API Health Check """

    response = {
        'status': 'OK',
        'response': 'Fast API service for signups and Telegram integration',
        'time': datetime.utcnow().isoformat()
    }
    return response