from django.db import models
from django.db.models import Q
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.utils.timezone import now

class Category(models.Model):
    name        = models.CharField('Category', max_length=150)
    description = models.TextField('Description')
    slug        = models.SlugField(max_length=100, unique=True, default='', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(category_pre_save_receiver, sender=Category)