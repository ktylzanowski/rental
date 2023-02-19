from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rental.settings')
app = Celery('rental')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Warsaw')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'check-rent-every-minute': {
        'task': 'products.tasks.send_mail_func',
        'schedule': 60.0,
    },
}
