from django.urls import path
from . import views

urlpatterns = [
    path('popular/', views.get_popular_movies, name='get_popular_movies'),
    path('watched/', views.watched_movies, name='watched_movies'),
    path('liked/', views.liked_movies, name='liked_movies'),
    path('<int:movie_pk>/watch/', views.toggle_watch, name='toggle_watch'),
    path('<int:movie_pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:movie_pk>/detail/', views.movie_detail, name='movie_detail'),
    # path('analyze-voice/', views.analyze_voice, name='analyze-voice'),
]