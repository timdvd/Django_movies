from django.db import models
from django.utils.timezone import now
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

class Genre(models.Model):
    name            = models.CharField('Name', max_length=100)
    description     = models.TextField('Description')
    slug            = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

def genre_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(genre_pre_save_receiver, sender=Genre)