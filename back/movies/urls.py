from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_movies, name='get_all_movies'),
    path('popular/', views.get_popular_movies, name='get_popular_movies'),
    path('watched/', views.watched_movies, name='watched_movies'),
    path('liked/', views.liked_movies, name='liked_movies'),
    path('<int:movie_pk>/watch/', views.toggle_watch, name='toggle_watch'),
    path('<int:movie_pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:movie_pk>/detail/', views.movie_detail, name='movie_detail'),
    path('analyze_voice/', views.analyze_voice, name='analyze-voice'),
    path('reviews/', views.review_list_create, name='review_list_create'), # 리뷰 목록 조회 및 생성(CR)
    path('reviews/<int:pk>/', views.review_detail_update_delete, name='review_detail_update_delete'), # 리뷰 상세 조회, 수정, 삭제(RUD),
    path('reviews/<int:review_pk>/like/', views.toggle_review_like, name='toggle_review_like'), # 리뷰 좋아요 버튼
    path('search/', views.search_movies_by_title, name='search_movies_by_title'),
    path('user-reviews/', views.user_reviews, name='user_reviews'),  # 사용자가 작성한 리뷰
    path('liked-reviews/', views.liked_reviews, name='liked_reviews'),  # 사용자가 좋아요한 리뷰
]