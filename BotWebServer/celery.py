import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BotWebServer.settings')

app = Celery('BotWebServer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'scheduled': {
        'task': 'core.tasks.del_task',
        # 'schedule': crontab(minute=0, hour=0) # noqa запустится в полночь
        'schedule': crontab(minute='*/5')  # noqa запустится в полночь

    }
}

app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()
