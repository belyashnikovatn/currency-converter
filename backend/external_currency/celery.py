"""Модуль для настройки celery."""
import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_converter.settings')

app = Celery('currency_converter')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_load_currencies(sender, **kwargs):
    sender.send_task(
        'external_currency.tasks.load_currencies'
    )


app.conf.beat_schedule = {
    'load_currencies': {
        'task': 'external_currency.tasks.load_currencies',
        'schedule': timedelta(hours=4),
    },
}
