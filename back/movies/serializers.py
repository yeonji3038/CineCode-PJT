from rest_framework import serializers
from .models import Movie, WatchedMovie, LikedMovie
from .models import Review
from django.contrib.auth.models import User
from movies.models import Movie

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


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster_path = serializers.CharField(source='movie.poster_path', read_only=True)
    is_liked = serializers.SerializerMethodField()
    liked_at = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'id', 'content', 'created_at', 'updated_at', 'likes',
            'is_spoiler', 'username', 'movie_title', 'movie_poster_path',
            'is_liked', 'liked_at', 'movie'
        ]

    def get_user(self, obj):
        return {
            'username': obj.user.username,
            'profile_image': obj.user.profile_image.url if obj.user.profile_image else None
        }


    def get_is_liked(self, obj):
        return hasattr(obj, 'user_likes') and len(obj.user_likes) > 0

    def get_liked_at(self, obj):
        if hasattr(obj, 'user_likes') and obj.user_likes:
            return obj.user_likes[0].created_at
        return None