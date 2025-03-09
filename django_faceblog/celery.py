from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_faceblog.settings')

app = Celery('django_faceblog')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'flush-expire-tokens-every-day-at-12': {
        'task': 'auth_system.tasks.flush_expired_tokens',
        'schedule': crontab(hour='12', minute='0'),
    }
}

app.autodiscover_tasks()
