from celery import shared_task
from .models import Movie

@shared_task(name='task_calculate_movie_rating')
def task_calculate_movie_rating(all=False , count = None):
    qs = Movie.objects.needs_updating()
    if all:
        qs = qs = Movie.objects.all()
    qs = qs.order_by('rating_last_updated')
    if isinstance(count , int):
        qs = qs[:count]
    for obj in qs:
        obj.calculate_rating(save=True)

