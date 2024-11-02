from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from .models import Rating
from django.views.decorators.http import require_http_methods
# Create your views here.

@require_http_methods(['POST'])
def rate_movie_view(request):
    if not request.htmx:
        return HttpResponse('Not Allowed' , status=400)
    object_id = request.POST.get('object_id')
    rating_value = request.POST.get('rating_value')
    message = "You must <a href='/account/login'>login</a> to rate this" 
    user = request.user
    if user.is_authenticated:
        message = '<span class="bg-danger text-light py-1 px-3 rounded">An Error Occured.</div>'
        ct = ContentType.objects.get(app_label='movies' , model='movie')
    
        rating_obj = Rating.objects.create(content_type=ct , object_id = object_id , value=rating_value , user=user)

        if rating_obj.content_object is not None:
            message = '<span class="bg-success text-light py-1 px-3 rounded">Rating Saved</div>'

        
    return HttpResponse(message, status=200)
