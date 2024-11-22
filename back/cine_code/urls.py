"""
URL configuration for cine_code project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views  # accounts 앱의 views를 import 해야 합니다
from movies import views as movies_views  # movies 앱의 views 추가
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('dj_rest_auth.urls')), 
    path('movies/', include('movies.urls')),
    path('community/', include('community.urls')),
    path('accounts/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='user-profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
