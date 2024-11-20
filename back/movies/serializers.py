from rest_framework import serializers
from .models import Movie, WatchedMovie, LikedMovie

class MovieSerializer(serializers.ModelSerializer):
    poster_path = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path',)
    
    def get_poster_path(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None


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