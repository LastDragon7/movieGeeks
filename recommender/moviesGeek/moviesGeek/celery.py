import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesGeek.settings')

app = Celery('moviesGeek')

app.config_from_object('django.conf:settings' , namespace='CELERY')

app.autodiscover_tasks()