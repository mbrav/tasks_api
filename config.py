
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

env_path = Path('.env')
load_dotenv(dotenv_path=env_path)


PRODUCTION = os.getenv('PRODUCTION', False)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', None)


if PRODUCTION:
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWORD = os.getenv('DB_PASSWORD', None)
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_NAME = os.getenv('DB_NAME', None)
    DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
else:
    DATABASE_URL = 'sqlite:///./api.db'

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    # datefmt='%d-%b-%y %H:%M:%S',
    format='%(levelname)s:%(name)s %(asctime)s: %(message)s')

logger = logging.getLogger(__name__)

app = FastAPI(
    title='API service for signups and Telegram integration',
    docs_url='/docs',
    version='0.1.0',
    redoc_url='/redocs'
)
