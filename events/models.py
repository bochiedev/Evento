from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from evento.utils import unique_slug_generator

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    venue = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)



def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(slug_save, sender=Event)
