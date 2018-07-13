import asyncio
from datetime import timedelta, time

from sanic import Sanic
from sanic_scheduler import task, SanicScheduler


app = Sanic()
scheduler = SanicScheduler(app)


@task(timedelta(seconds=30))
def hello(app):
    """Runs the function every 30 seconds."""
    print("Hello, {0}".format(app))


@task(timedelta(hours=1), time(hour=1, minute=30))
async def foo_bar(_):
    """Runs the function every 1 hours after 1:30."""
    print("Foo")
    await asyncio.sleep(1)
    print("Bar")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
