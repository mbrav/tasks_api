
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)


DEBUG = os.getenv('DEBUG', False)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
# DATABASE_URL = 'sqlite:///./api.db'

logging.basicConfig(
    filename='app.log',
    level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.0',
    redoc_url='/redocs'
)
