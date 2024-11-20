from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Movie, WatchedMovie, LikedMovie
from .serializers import MovieSerializer, WatchedMovieSerializer, LikedMovieSerializer

TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

@api_view(['GET'])
def get_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watched_movies(request):
    watched = WatchedMovie.objects.filter(user=request.user).order_by('-watched_at')
    serializer = WatchedMovieSerializer(watched, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    liked = LikedMovie.objects.filter(user=request.user).order_by('-liked_at')
    serializer = LikedMovieSerializer(liked, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_watch(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    watched = WatchedMovie.objects.filter(user=request.user, movie=movie)
    
    if watched.exists():
        watched.delete()
        return Response({'message': '시청 목록에서 제거됨'})
    else:
        WatchedMovie.objects.create(user=request.user, movie=movie)
        return Response({'message': '시청 목록에 추가됨'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    liked = LikedMovie.objects.filter(user=request.user, movie=movie)
    
    if liked.exists():
        liked.delete()
        return Response({'message': '찜 목록에서 제거됨'})
    else:
        LikedMovie.objects.create(user=request.user, movie=movie)
        return Response({'message': '찜 목록에 추가됨'})


