from django.urls import path, include
from .views import ActorView

urlpatterns = [
    path('<slug:slug>/', ActorView.as_view(), name='actor_detail'),
]