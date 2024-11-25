from rest_framework import serializers
from .models import Movie, WatchedMovie, LikedMovie
from .models import Review
from django.contrib.auth.models import User
from movies.models import Movie
from django.contrib.auth import get_user_model

TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
User = get_user_model()

class MovieSerializer(serializers.ModelSerializer):
    poster_path = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
    
    def get_poster_path(self, obj):
        if not obj.poster_path:
            return None
        # 이미 전체 URL인 경우
        if obj.poster_path.startswith(('http://', 'https://')):
           return obj.poster_path
        # 상대 경로인 경우 기본 URL 추가
        return f"{TMDB_IMAGE_BASE_URL}{obj.poster_path}"
    
    # def get_genres(self, obj):
    #     return [genre.name for genre in obj.genres.all()]


class WatchedMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    
    class Meta:
        model = WatchedMovie
        fields = ('movie', 'watched_at',)


class LikedMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    
    class Meta:
        model = LikedMovie
        fields = ('movie', 'liked_at',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']


class MovieSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_path']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSimpleSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.CharField(source='user.profile_image', read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'content', 'created_at', 'updated_at', 
            'likes', 'is_spoiler', 'user', 'movie', 'is_liked', 'username', 'profile_image'
        ]
        read_only_fields = ['user', 'likes']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if hasattr(obj, 'user_likes'):
                return len(obj.user_likes) > 0
            return obj.liked_by.filter(user=request.user).exists()
        return False