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
    profile_image = serializers.CharField(source='user.profile_image', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'content', 'is_spoiler', 'movie', 'user', 'created_at', 
                 'username', 'profile_image', 'likes', 'is_liked']
        read_only_fields = ['user', 'likes']

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.liked_reviews.filter(user=request.user).exists()
        return False