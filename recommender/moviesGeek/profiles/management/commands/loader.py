from typing import Any
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from moviesGeek.utils import *
from movies.models import *
User = get_user_model()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('count' , nargs='?' , default=10 , type=int)
        parser.add_argument('--movies' , action='store_true' , default=False)
        parser.add_argument('--users' , action='store_true' , default=False)
        parser.add_argument('--show-total' , action='store_true' , default=False)
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')
        if load_movies:
            movies_data = load_movie_data(limit=count)
            movies_new = [Movie(**x) for x in movies_data]
            movies_bulk = Movie.objects.bulk_create(movies_new , ignore_conflicts=True)
            print(f'new movies added {len(movies_bulk)}')
            if show_total:
                print(f'Total Movies : {Movie.objects.count()}')
        if generate_users:
            profiles = get_fake_profile(count=count)
            
            new_users = []
            for profile in profiles:
                new_users.append(User(**profile))
            
            user_bulk = User.objects.bulk_create(new_users , ignore_conflicts=True)

            print(f'new user created {len(user_bulk)}')
            if show_total:
                print(f'Users : {User.objects.count()}')