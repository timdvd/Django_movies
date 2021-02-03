from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, CreateView
from .models import Movie, Genre, Rating, RatingStar, Review
from category.models import Category
from django.http import Http404
from django.http import JsonResponse, HttpResponse
from .forms import ReviewForm, RatingForm
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')

class MovieListView(GenreYear, ListView):
    model = Movie
    template_name = 'home.html'
    ordering = ['-timestamp']
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(MovieListView, self).get_context_data(*args, **kwargs)
        context['movies'] = Movie.objects.all()
        context['title'] = 'Home'
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Movie.objects.all().filter(active=True)

def movieComment(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        user = request.user
        movieId = request.POST.get('movieId')
        movie = Movie.objects.get(id=movieId)
        if text == '':
            messages.error(request, 'Enter your text!')
            return redirect(f"/movie/{movie.slug}")
        else:
            review = Review(text=text, user=user, movie=movie)
            review.save()
            messages.success(request, 'Your comment has been posted!')

    return redirect(f"/movie/{movie.slug}")

class MovieSlugView(GenreYear, DetailView):
    queryset = Movie.objects.all()
    template_name = 'movie/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(MovieSlugView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Movie'
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        context['reviews'] = Review.objects.order_by('pk')
        slug = self.kwargs.get('slug')
        movie_obj = Movie.objects.get(slug=slug)
        return context

    def get_object(self, *args, **kwargs):
        request =self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Movie.objects.get(slug=slug, active=True)
        except Movie.DoesNotExist:
            raise Http404('Not found')
        except Movie.MultipleObjectsReturned:
            qs = Movie.objects.filter(slug=slug, active=True)
            instance = qs.first()
        return instance



class FilterMoviesView(GenreYear, ListView):
    paginate_by = 9
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class SearchListView(ListView):
    paginate_by = 9
    template_name = 'movie/result.html'
    
    def get_queryset(self, *args, **kwargs):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super(SearchListView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context