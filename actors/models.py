from django.db import models
from django.utils.timezone import now
from PIL import Image
from .utils import unique_slug_generator
from django.db.models.signals import pre_save

class Actor(models.Model):
    name        = models.CharField("Name", max_length=100)
    age         = models.PositiveSmallIntegerField('Age', default=0)
    description = models.TextField("Description")
    image       = models.ImageField("Image", upload_to='actors/')
    active      = models.BooleanField('Active', default=True)
    slug        = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 420 or img.width > 400:
            output_size = (420, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


    class Meta:
        verbose_name = 'Actors and directors'
        verbose_name_plural = 'Actors and directors'
    
def actor_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(actor_pre_save_receiver, sender=Actor)