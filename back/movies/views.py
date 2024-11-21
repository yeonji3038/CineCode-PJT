from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Movie, WatchedMovie, LikedMovie
from .serializers import MovieSerializer, WatchedMovieSerializer, LikedMovieSerializer
import requests
# from google.cloud import language_v1
# import os
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
from google.cloud import speech_v1
from google.cloud import language_v1
import json


TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'


@api_view(['GET'])
def get_movies(request):
    movies = Movie.objects.order_by('-popularity')[:50]  # 인기 순으로 50개만 가져오기
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
    youtube_api_key = settings.YOUTUBE_API_KEY
    
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
    if youtube_data.get('items'):
        response_data['trailer_id'] = youtube_data['items'][0]['id']['videoId']
    
    return Response(response_data)


#음성인식


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

# def analyze_sentiment(text):
#     client = language_v1.LanguageServiceClient()
#     document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
#     sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
#     return sentiment.score  # 감정 점수 반환

# #TMDB API 호출을 통한 영화 추천
# def get_movie_recommendations(genre_id):
#     url = f'https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}'
#     response = requests.get(url)
#     return response.json()

# def recommend_movies_based_on_sentiment(score):
#     if score > 0:
#         genre_id = 10749  # 로맨스
#     else:
#         genre_id = 28  # 액션
#     return get_movie_recommendations(genre_id)

# #전체흐름
# @csrf_exempt
# def analyze_sentiment_view(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         text = data.get('text')

#         # 감정 분석
#         score = analyze_sentiment(text)

#         # 감정 분석 결과에 따라 영화 추천
#         recommended_movies = recommend_movies_based_on_sentiment(score)

#         return JsonResponse({
#             "emotion_score": score,
#             "recommended_movies": recommended_movies
#         })


@api_view(['POST'])
def analyze_voice(request):
    try:
        client = speech_v1.SpeechClient(credentials=settings.GOOGLE_CLOUD_CREDENTIALS)
        
        audio = speech_v1.RecognitionAudio(content=request.FILES['audio'].read())
        config = speech_v1.RecognitionConfig(
            encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="ko-KR",
        )
        
        response = client.recognize(config=config, audio=audio)
        
        # 음성 인식 결과가 있는지 확인
        if not response.results:
            return Response({'error': '음성을 인식할 수 없습니다.'}, status=400)
            
        text = response.results[0].alternatives[0].transcript
        
        # Natural Language API로 감정 분석
        language_client = language_v1.LanguageServiceClient(credentials=settings.GOOGLE_CLOUD_CREDENTIALS)
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = language_client.analyze_sentiment(request={'document': document})
        
        score = sentiment.document_sentiment.score
        
        # 감정 점수에 따른 장르 선택
        if score > 0.3:
            genres = [35, 10749]  # 코미디, 로맨스
        elif score < -0.3:
            genres = [28, 12]  # 액션, 어드벤처
        else:
            genres = [18, 99]  # 드라마, 다큐멘터리

        # TMDB API로 영화 추천
        tmdb_api_key = settings.TMDB_API_KEY
        movies = []
        for genre in genres:
            url = f'https://api.themoviedb.org/3/discover/movie'
            params = {
                'api_key': tmdb_api_key,
                'with_genres': genre,
                'language': 'ko-KR'
            }
            response = requests.get(url, params=params)
            movies.extend(response.json()['results'])
        
        return Response({
            'text': text,
            'sentiment': score,
            'movies': movies[:10] if movies else []  # movies가 비어있을 경우 처리
        })
        
    except IndexError as e:
        return Response({'error': '음성 인식 결과를 처리할 수 없습니다.'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=400)