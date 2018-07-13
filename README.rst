SanicScheduler
==============

SanicScheduler runs a functions on a schedule.

Installation
------------

Automatic installation:

.. code:: bash

   $ pip install sanic-scheduler

SanicScheduler is listed in `PyPI`_ and can be installed with pip or
easy_install.

Manual installation:

.. code:: bash

   $ git clone https://github.com/asmodius/sanic-scheduler.git
   $ cd sanic_scheduler
   $ python setup.py install

SanicScheduler source code is `hosted on GitHub`_

Usage
-----

.. code:: python

   import asyncio
   from datetime import timedelta, time

   from sanic import Sanic
   from sanic_scheduler import SanicScheduler, task

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

.. _PyPI: https://pypi.python.org/pypi/sanic-scheduler
.. _hosted on GitHub: https://github.com/asmodius/sanic-scheduler
