from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import user_register, user_login, profile

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', user_register, name='register'), 
    path('profile/', profile, name='profile'),
]
