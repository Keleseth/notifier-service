import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifier_service.settings')

app = Celery('notifier_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
print(f"Celery broker: {app.conf.broker_url}")
app.autodiscover_tasks()
