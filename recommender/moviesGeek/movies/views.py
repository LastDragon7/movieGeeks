from django.shortcuts import render
from django.views import generic
from .models import Movie

SORTING_CHOICES = {
    "popular": "-rating_avg",
    "unpopular": "rating_avg",
    "recent": "-release_date",
    "old": "release_date"
}

class MovieListView(generic.ListView):
    paginate_by = 100

    def get_queryset(self):
        request = self.request
        default_sort = request.session.get('movie_sort_order') or '-rating_avg'
        qs = Movie.objects.all().order_by(default_sort)
        sort = request.GET.get('sort')
        if sort is not None:
            request.session['movie_sort_order'] = sort
            qs = qs.order_by(sort)
        return qs

    def get_template_names(self):
        request = self.request
        if request.htmx:
            return ['movies/snippet/list.html']
        return ['movies/list_view.html']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        context['sorting_choices'] = SORTING_CHOICES
        if user.is_authenticated:
            object_list = context['object_list']
            object_ids = [x.id for x in object_list]
            my_ratings =  user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context['my_ratings'] = my_ratings
        return context

class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    queryset = Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        user = request.user
        if user.is_authenticated:
            object = context['object']
            object_ids = [object.id]
            my_ratings =  user.rating_set.movies().as_object_dict(object_ids=object_ids)
            context['my_ratings'] = my_ratings
        return context
