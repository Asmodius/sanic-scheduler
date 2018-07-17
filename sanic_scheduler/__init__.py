import asyncio
import inspect
import logging
import traceback
from datetime import datetime, time, timedelta
from typing import Optional, Union


__version__ = '1.0.4'

__all__ = ('task', 'SanicScheduler')

logger = logging.getLogger('scheduler')

_tasks = []
_wrk = []


def task(period: timedelta,
         start: Optional[Union[timedelta, time]] = None):
    """Decorate the function to run on schedule."""
    def wrapper(fn):
        _tasks.append(Task(fn, period, start))
        return fn
    return wrapper


class SanicScheduler:
    def __init__(self, app=None, utc=True):
        self.app = app
        if app:
            self.init_app(app, utc)

    def init_app(self, app, utc=True):
        self.app = app

        @app.listener("after_server_start")
        async def run_scheduler(_app, loop):
            for i in _tasks:
                _wrk.append(loop.create_task(i.run(_app, utc)))

        @app.listener("before_server_stop")
        async def stop_scheduler(_app, _):
            for i in _wrk:
                i.cancel()

        return self


class Task:
    def __init__(self, func, period, start):
        self.func = func
        self.func_name = func.__name__
        self.period = period
        self.start = start
        self.last_run = None

    def _next_run(self, utc):
        if utc:
            now = datetime.utcnow().replace(microsecond=0)
        else:
            now = datetime.now().replace(microsecond=0)

        if self.last_run is None:
            if self.start is not None:
                if isinstance(self.start, time):
                    d1 = datetime.combine(datetime.min, self.start)
                    d2 = datetime.combine(datetime.min, now.time())
                    self.start = timedelta(seconds=(d1 - d2).seconds)

                self.last_run = now + self.start - self.period
            else:
                self.last_run = now

        while self.last_run <= now:
            self.last_run += self.period

        return self.last_run - now

    async def run(self, app, utc=True):
        while True:
            delta = self._next_run(utc)
            logger.debug('NEXT TASK "%s" %s' % (self.func_name, delta))
            await asyncio.sleep(delta.seconds)
            logger.info('RUN TASK "%s"' % self.func_name)
            try:
                ret = self.func(app)
                if inspect.isawaitable(ret):
                    await ret
                logger.info('END TASK "%s"' % self.func_name)
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
