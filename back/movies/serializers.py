from rest_framework import serializers
from .models import Movie, WatchedMovie, LikedMovie
from .models import Review
from django.contrib.auth.models import User
from movies.models import Movie
from django.contrib.auth import get_user_model

User = get_user_model()

class MovieSerializer(serializers.ModelSerializer):
    poster_path = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'
    
    def get_poster_path(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None
    
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
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'content', 'created_at', 'updated_at', 
            'likes', 'is_spoiler', 'user', 'movie', 'is_liked'
        ]

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if hasattr(obj, 'user_likes'):
                return len(obj.user_likes) > 0
            return obj.liked_by.filter(user=request.user).exists()
        return False