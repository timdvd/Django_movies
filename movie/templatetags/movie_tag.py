from django import template
from category.models import Category
from ..models import Movie

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('snippets/last_movies.html')
def get_last_movies():
    movies = Movie.objects.order_by('id')[:3]
    return {'last_movies': movies}
