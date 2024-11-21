from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Movie, WatchedMovie, LikedMovie
from .serializers import MovieSerializer, WatchedMovieSerializer, LikedMovieSerializer
import requests
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

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    tmdb_api_key = settings.TMDB_API_KEY
    youtube_api_key = settings.YOUTUBE_API_KEY
    
    # TMDB에서 배경 이미지 가져오기
    tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_pk}'
    tmdb_response = requests.get(tmdb_url, params={
        'api_key': tmdb_api_key,
        'language': 'ko-KR'
    })
    tmdb_data = tmdb_response.json()
    
    # YouTube에서 예고편 검색
    youtube_url = 'https://www.googleapis.com/youtube/v3/search'
    youtube_response = requests.get(youtube_url, params={
        'key': youtube_api_key,
        'q': f'{movie.title} 예고편',
        'part': 'snippet',
        'maxResults': 1,
        'type': 'video'
    })
    youtube_data = youtube_response.json()
    
    # 응답 데이터 구성
    response_data = MovieSerializer(movie).data
    response_data['backdrop_path'] = tmdb_data.get('backdrop_path')
    response_data['runtime'] = tmdb_data.get('runtime')
    response_data['genres'] = [genre.get('name') for genre in tmdb_data.get('genres', [])]
    if youtube_data.get('items'):
        response_data['trailer_id'] = youtube_data['items'][0]['id']['videoId']
    
    return Response(response_data)
