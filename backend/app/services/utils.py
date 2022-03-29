import functools
import logging
import time

logger = logging.getLogger(__name__)


def timer(func):
    """Timer Decorator"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        run_time = time.perf_counter() - start_time
        logger.info(f'{func.__name__} processed in {run_time:.4f} seconds.')
        return value

    return wrapper_timer
