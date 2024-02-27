import os
import logging

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wsaude.settings')

app = Celery('wsaude')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    logging.info(f'Request: {self.request!r}')
