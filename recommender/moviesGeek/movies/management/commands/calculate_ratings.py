from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from moviesGeek.utils import *
from movies.models import *
# from movies.tasks import task_calculate_movie_rating
from ratings.tasks import task_update_movie_rating
User = get_user_model()

class Command(BaseCommand):
    def handle(self , *args , **options):
        task_update_movie_rating()