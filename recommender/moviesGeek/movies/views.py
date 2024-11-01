from django.shortcuts import render
from django.views import generic
from .models import Movie

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    paginate_by = 100
    queryset = Movie.objects.all().order_by('-rating_avg')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            my_ratings =  user.rating_set.filter(active = True).as_object_dict(object_ids = object_ids)
            context['my_ratings'] = {f'{x.object_id}' : x.value for x in my_ratings}
        return context

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    queryset = Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            objects = context['object']
            object_ids = [objects.id]
            my_ratings =  user.rating_set.filter(active = True).as_object_dict(object_ids = object_ids)
            context['object'] = {f'{x.object_id}' : x.value for x in my_ratings}
        return context
