from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_movies, name='get_movies'),
    path('watched/', views.watched_movies, name='watched_movies'),
    path('liked/', views.liked_movies, name='liked_movies'),
    path('<int:movie_pk>/watch/', views.toggle_watch, name='toggle_watch'),
    path('<int:movie_pk>/like/', views.toggle_like, name='toggle_like'),
]