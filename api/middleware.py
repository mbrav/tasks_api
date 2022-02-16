import logging
import random
import time

from fastapi import Request, middleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add request process time to response headers"""

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = '{0:.5f}'.format(time.time() - start_time)
        response.headers['X-Process-Time'] = str(process_time)
        print(f'Process Time: {process_time}ms')
        return response


class LoggerMiddleware(BaseHTTPMiddleware):
    """Add request logging to response headers"""

    async def dispatch(self, request, call_next):
        logger.info(f'Start request path={request.url.path}')
        start_time = time.time()

        response = await call_next(request)

        process_time = '{0:.5f}'.format(time.time() - start_time)
        logger.info(
            f'Process Time: {process_time}s status_code={response.status_code}')

        return response
