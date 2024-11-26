from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    # path('find_id/', views.find_id, name='find_id'),
    # path('google/', views.google, name='google'),
    # path('naver/', views.get_naver_info, name='naver'),
    path('google/', views.google, name='google_login'),
] 