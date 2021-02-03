from django.urls import path, include
from .views import MovieSlugView, MovieListView, FilterMoviesView, AddStarRating, SearchListView, movieComment

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path('movie/<slug:slug>/', MovieSlugView.as_view(), name='movie_detail'),
    path('search/', SearchListView.as_view(), name='search'),
    path('review', movieComment, name='PostComment'),
]