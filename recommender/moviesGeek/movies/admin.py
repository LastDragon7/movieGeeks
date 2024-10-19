from django.contrib import admin

# Register your models here.
from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'calc_ratings_count']
    readonly_fields = ['calc_ratings_count' , 'rating_avg_display']

admin.site.register(Movie , MovieAdmin)