# Sanic Scheduler

Sanic Scheduler runs a functions on a schedule.

## Installation

Automatic installation:
```bash
$ pip install sanic-scheduler
```

Sanic Scheduler is listed in [PyPI](https://pypi.python.org/pypi/sanic-scheduler) and can be installed with pip or easy_install.

Manual installation:
```bash
$ git clone https://github.com/asmodius/sanic-scheduler.git
$ cd sanic_scheduler
$ python setup.py install
```

Sanic Scheduler source code is [hosted on GitHub](https://github.com/asmodius/sanic-scheduler)

## Usage

```python
import asyncio
from datetime import datetime, time, timedelta

from sanic import Sanic

from sanic_scheduler import SanicScheduler, task


app = Sanic()
scheduler = SanicScheduler(app)


@task(timedelta(seconds=30))
def hello(app):
    """Runs the function every 30 seconds."""
    print("Hello, {0}".format(app), datetime.now())


@task(timedelta(hours=1), time(hour=1, minute=30))
async def foo_bar(_):
    """Runs the function every 1 hours after 1:30."""
    print("Foo", datetime.now())
    await asyncio.sleep(1)
    print("Bar")


@task(timedelta(minutes=2), timedelta(seconds=10))
def baz(_):
    """Runs the function every 2 minutes after 10 seconds."""
    print("Baz", datetime.now())


@task(start=timedelta(seconds=10))
def another(_):
    """Run the function after 10 seconds once."""
    print("another", datetime.now())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
```
