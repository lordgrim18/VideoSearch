from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VideoSearch.settings')

app = Celery('VideoSearch')
app.conf.enable_utc = False
app.conf.update(
    timezone='Asia/Kolkata',
    task_concurrency=4,
    worker_prefetch_multiplier=5,
    )
app.conf.broker_connection_retry_on_startup = True
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')