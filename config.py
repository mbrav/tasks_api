
from fastapi import FastAPI

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.0',
    redoc_url='/redocs'
)
