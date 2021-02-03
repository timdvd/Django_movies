from django.db import models
from actors.models import Actor
from users.models import User
from genre.models import Genre
from category.models import Category
from django.db.models import Q
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from datetime import date
from PIL import Image
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class MovieQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def featured(self):
        return self.filter(featured=True, active=True)

class MovieManager(models.Manager):
    def get_queryset(self):
        return MovieQuerySet(self.model, using=self._db)
    def all(self):
        return self.get_queryset().active()

class Movie(models.Model):
    title           = models.CharField('Title', max_length=100)
    tagline         = models.CharField('Slogan', max_length=100)
    description     = models.TextField('Description')
    poster          = models.ImageField('Poster', upload_to='movies/')
    year            = models.PositiveSmallIntegerField('Date', default=2019)
    country         = models.CharField('Country', max_length=30)
    directors       = models.ManyToManyField(Actor, verbose_name='director', related_name='film_director')
    actors          = models.ManyToManyField(Actor, verbose_name='actors', related_name='film_actor')
    genre           = models.ManyToManyField(Genre, verbose_name='genres')
    world_premiere  = models.DateField('World Primere', default=date.today)
    budget          = models.PositiveIntegerField('Budget', default=0, help_text='sum in dollars')
    fees_in_usa     = models.PositiveIntegerField('Fees in USA', default=0, help_text='sum in dollars')
    fees_in_world   = models.PositiveIntegerField('Fees in World', default=0, help_text='sum in dollars')
    category        = models.ForeignKey(Category, verbose_name='Category', on_delete=models.SET_NULL, null=True)
    slug            = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    draft           = models.BooleanField('Draft', default=False)
    active          = models.BooleanField('Active', default=True)
    timestamp       = models.DateTimeField('Date', default=timezone.now)

    objects = MovieManager()
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.slug})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True).order_by('-timestamp')
    
    def save(self):
        super().save()

        img = Image.open(self.poster.path)

        if img.height > 420 or img.width > 300:
            output_size = (300, 420)
            img.thumbnail(output_size)
            img.save(self.poster.path)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
    

def movie_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(movie_pre_save_receiver, sender=Movie)


class MovieShots(models.Model):
    title       = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    image       = models.ImageField('Image', upload_to='movie_shots/')
    movie       = models.ForeignKey(Movie, verbose_name='Film', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movie Shot'
        verbose_name_plural = 'Movie Shots'

class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Value', default=0,
        validators = [
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Rating Star'
        verbose_name_plural = 'Rating Stars'  
        ordering = ['-value']  

class Rating(models.Model):
    ip      = models.CharField('Ip address', max_length=15)
    star    = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='star')
    movie   = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='movie')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
    

class Review(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    movie       = models.ForeignKey(Movie, verbose_name='movie', on_delete=models.CASCADE)
    text        = models.TextField('Message', max_length=5000)
    parent      = models.ForeignKey('self', verbose_name='Parent', on_delete=models.SET_NULL, blank=True, null=True)
    timestamp   = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.movie}"

    class Meta:
       ordering = ('-timestamp')
    
    def get_absolute_url(self):
        return reverse("home")
    
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
