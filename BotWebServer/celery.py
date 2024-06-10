import os

from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BotWebServer.settings')

app = Celery('BotWebServer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'del-every-daily-at-midnight.': {
        'task': 'core.tasks.del_task',
        # 'schedule': crontab(minute=0, hour=0) # noqa запустится в полночьx\
        'schedule': crontab(minute='*/5')  # noqa запустится в полночь

    },
    'update-every-15-minutes.': {
        'task': 'core.tasks.update_reports_data',
        'schedule': crontab(minute='*/1')  # noqa запустится в полночь
    }

}

app.conf.timezone = 'Europe/Moscow'

app.autodiscover_tasks()
