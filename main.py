import uvicorn

from api import db, models
from api.routers import router
from config import app

app.include_router(router)
models.Base.metadata.create_all(db.engine)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
