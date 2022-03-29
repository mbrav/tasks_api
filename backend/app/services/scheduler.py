import asyncio
import logging
from typing import Callable

from app import db, models
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)


def test_task():
    logger.info('EXECUTING TASK')


class SchedulerService:
    """Scheduler service"""

    def __init__(self, workers: int = 2):
        self.workers = workers
        self.queue = asyncio.Queue()
        self.scheduler = AsyncIOScheduler()
        self.db_session = db.Session()

    async def process_task(self):
        loop = asyncio.get_event_loop()
        while True:
            task = await self.queue.get()
            logger.info(f'Processing task "{task.__name__}"...')
            await loop.run_in_executor(None, task)
            self.queue.task_done()

    async def p_task(self):
        loop = asyncio.get_event_loop()
        print(f'Queue task len: {str(self.queue.qsize())}')
        while self.queue.qsize() > 0:
            task = await self.queue.get()
            logger.info(f'Processing task "{task.__name__}"...')
            result = await loop.run_in_executor(None, task)
            self.queue.task_done()
            return result

    async def get_executable_tasks(self):
        try:
            db_tasks = await models.Task.get_executable_tasks(self.db_session)
            result = db_tasks.scalars().all()
            for row in result:
                print(
                    f'#{row.id} - {row.name} ({row.status}) {row.created_at} {row.planned_for}')
        except Exception as ex:
            print(ex)

    async def gather_tasks(self):
        loop = asyncio.get_event_loop()
        print(f'Queue task len: {str(self.queue.qsize())}')
        while self.queue.qsize() > 0:
            task = await self.queue.get()
            logger.info(f'Processing task "{task.__name__}"...')
            result = await loop.run_in_executor(None, task)
            self.queue.task_done()
            return result

    async def start(self):
        self.scheduler.start()
        # self.scheduler.add_job(
        #     self.gather_tasks,
        #     'interval',
        #     seconds=5,
        #     max_instances=1)
        # self.scheduler.add_job(
        #     lambda: self.scheduler.print_jobs(),
        #     'interval', seconds=5)
        # self.scheduler.add_job(
        #     lambda: print(f'Queue task len: {str(self.queue.qsize())}'),
        #     'interval', seconds=5)
        # self.scheduler.add_job(
        #     lambda: self.queue.put_nowait(test_task),
        #     'interval', seconds=2)
        self.scheduler.add_job(
            self.get_executable_tasks,
            'interval', seconds=2, max_instances=1)

    async def add_task(self, func: Callable = test_task, name: str = None, **kwargs):
        if not name:
            name = func.__name__
        logger.info(f'Queueing task "{name}."')
        self.queue.put_nowait(func)


scheduler = SchedulerService()


async def start_scheduler():
    logger.info('Scheduler service startup BEGIN')
    await scheduler.start()
    logger.info('Scheduler service startup DONE')


# Dependency
async def get_scheduler() -> SchedulerService:
    yield scheduler
