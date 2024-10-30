import random
from celery import shared_task
from movies.models import Movie
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg , Count
from django.utils import timezone
import time
import datetime

from .models import Rating , RatingChoice


User = get_user_model()

@shared_task(name='generate_fake_reviews')
def generate_fake_reviews(count=100 , users = 10 , null_avg = False):
    user_s = User.objects.first()
    user_e = User.objects.last()

    # random_user_ids = random.sample(range(user_s.id , user_e.id) , users)
    random_user_ids = random.sample(range(user_s.id, user_e.id), users)


    users = User.objects.filter(id__in=random_user_ids)

    movies = Movie.objects.all().order_by('?')[:count]

    movie_ctype = ContentType.objects.get_for_model(Movie)

    if null_avg:
        movies = Movie.objects.filter(rating_avg__isnull=True).order_by('?')[:count]
    n_rating = movies.count()
    rating_choices = [x for x in RatingChoice.values if x is not None]
    user_ratings = [random.choice(rating_choices) for _ in range(0 , n_rating)]

    new_ratings = []
    for movie in movies:
        rating_obj = Rating.objects.create(
            content_object =  movie,
            content_type = movie_ctype,
            object_id = movie.id,
            value = user_ratings.pop(),
            user = random.choice(users)
        )
        new_ratings.append(rating_obj.id)

    return new_ratings

@shared_task(name = 'task_update_movie_rating')
def task_update_movie_rating():
    s_time = time.time()
    ctype = ContentType.objects.get_for_model(Movie)
    ratings = Rating.objects.filter(content_type = ctype).values('object_id').annotate(average=Avg('value') , count=Count('object_id'))
    for rating in ratings:
        object_id = rating['object_id']
        count = rating['count']
        avg = rating['average']
        qs = Movie.objects.filter(id=object_id)
        qs.update(
            rating_last_updated = timezone.now() ,
            rating_avg = avg ,
            rating_count = count
        )
    e_time = time.time() - s_time
    delta = datetime.timedelta(seconds = int(e_time))
    print(f'time take {delta}   {e_time}s')