from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from moviesGeek.utils import *
from movies.models import *
from movies.tasks import task_calculate_movie_rating
User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--all' , action='store_true' , default=False)
        parser.add_argument('count' , nargs='?' , default=1_000 , type=int)
    
    def handle(self , *args , **options):
        count = options.get('count')
        all = options.get('all')
        task_calculate_movie_rating(all=all , count=count)