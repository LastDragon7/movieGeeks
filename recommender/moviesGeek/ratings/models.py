from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Avg
from django.utils import timezone
from django.apps import apps
# Create your models here.

User = settings.AUTH_USER_MODEL

class RatingChoice(models.IntegerChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    __empty__ = 'Rate This'

class RatingQuerySet(models.QuerySet):
    def avg(self):
        return self.aggregate(average=Avg('value'))['average'] # {'average' : values}
    
    def as_object_dict(self , object_ids = []):
        qs =  self.filter(object_id__in = object_ids)
        return {f'{x.object_id}' : x.value for x in qs}

    def movies(self):
        Movie = apps.get_model('movies' , 'Movie')
        ct = ContentType.objects.get_for_model(Movie)
        return self.filter(active = True , content_type = ct)

class RatingManager(models.Manager):
    def get_queryset(self):
        return RatingQuerySet(self.model , using=self._db)
    
    def movies(self):
        return self.get_queryset().movies()
    
    def avg(self):
        return self.get_queryset().avg()

class Rating(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    value = models.IntegerField(null=True , blank=True , choices=RatingChoice.choices)
    content_type = models.ForeignKey(ContentType , on_delete= models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type' , 'object_id')
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active_update_timestamp = models.DateTimeField(auto_now_add=False , null=True , blank=True , auto_now=False)

    objects = RatingManager()

    class Meta:
        ordering = ['-timestamp']

def rating_post_save(sender , instance , created , *args , **kwargs):
    if created:
        _id = instance.id
        if instance.active:
            q = Rating.objects.filter(content_type = instance.content_type ,
                                       object_id = instance.object_id ,
                                         user = instance.user
                                    ).exclude(id=_id , active=True)
            if q.exists():
                q = q.exclude(active_update_timestamp__isnull = False)
                q.update(active=False , active_update_timestamp = timezone.now())

post_save.connect(rating_post_save , sender=Rating)
            