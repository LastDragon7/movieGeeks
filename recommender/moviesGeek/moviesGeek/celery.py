import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviesGeek.settings')

app = Celery('moviesGeek')

app.config_from_object('django.conf:settings' , namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'run_movie_rating_avg' : {
        'task' : 'task_calculate_movie_rating',
        'schedule' : 60 * 30, # 30 minutes
        'kwargs' : {'count' : 20_000}
    }
}