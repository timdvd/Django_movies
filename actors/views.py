from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Actor
from movie.views import GenreYear
from django.http import Http404

# Create your views here.
class ActorView(DetailView):
    model = Actor
    template_name = 'actors/actor.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ActorView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Actor'
        slug = self.kwargs.get('slug')
        movie_obj = Actor.objects.get(slug=slug)
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Actor.objects.get(slug=slug, active=True)
        except Actor.DoesNotExist:
            raise Http404('Not found')
        except Actor.MultipleObjectsReturned:
            qs = Actor.objects.filter(slug=slug, active=True)
            instance = qs.first()
        return instance