from __future__ import absolute_import, unicode_literals
from celery import Celery
import json
import urllib
import urllib2
import os


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Servidor.settings')

from django.conf import settings  # noqa


app = Celery('Servidor',
             broker='amqp://',
             backend='amqp://',
             include=['ServidorApp.tasks'])

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    #sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(10.0, test.s(), expires=10)


@app.task
def test():
	data = json.dumps({"type":"5"})
	clen = len(data)
	req = urllib2.Request('http://127.0.0.1:8000/', data, {'Content-Type': 'application/json', 'Content-Length': clen})
	f = urllib2.urlopen(req)

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()