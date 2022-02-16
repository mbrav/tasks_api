import logging
import random
import time

from fastapi import Request, middleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    """Add request process time to response headers wiht logger"""

    async def dispatch(self, request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = '{0:.5f}'.format(time.time() - start_time)
        response.headers['X-Process-Time'] = str(process_time)

        log_message = f'Request "{request.url.path}" ' \
            f'{response.status_code} time {process_time}s '

        if response.status_code < 203:
            logger.info(log_message)
        elif response.status_code < 500:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        return response
