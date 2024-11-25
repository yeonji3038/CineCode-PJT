from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Movie, WatchedMovie, LikedMovie, Review, LikedReview
from .serializers import MovieSerializer, WatchedMovieSerializer, LikedMovieSerializer, ReviewSerializer
import requests
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.cloud import speech, language_v2
import os
from google.cloud import speech_v1
from google.cloud import language_v1
import json
import random
from pathlib import Path
from django.db.models import Prefetch


TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# 전체 영화 조회
@api_view(['GET'])
def get_all_movies(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)   


# 인기순 영화 40개 조회
@api_view(['GET'])
def get_popular_movies(request):
    movies = Movie.objects.all().order_by('-popularity')[:40]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# 시청중인 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def watched_movies(request):
    watched = WatchedMovie.objects.filter(user=request.user).order_by('-watched_at')
    serializer = WatchedMovieSerializer(watched, many=True)
    return Response(serializer.data)


# 찜한 영화 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_movies(request):
    liked = LikedMovie.objects.filter(user=request.user).order_by('-liked_at')
    serializer = LikedMovieSerializer(liked, many=True)
    return Response(serializer.data)


# 시청중인 영화 목록에서 제거
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


# 영화 찜하기 취소
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

# 영화 시청 상태 업데이트
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_movie_status(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    status = request.data.get('status')
    if status in ['미시청', '시청 중', '시청 완료']:
        movie.status = status
        movie.save()
        return Response({'message': '상태가 업데이트되었습니다.'})
    return Response({'error': '잘못된 상태 값입니다.'}, status=400)


# 영화 상세 정보 조회
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 현재 사용자의 재생/찜 상태 확인
    response_data = MovieSerializer(movie).data
    if request.user.is_authenticated:
        response_data['is_liked'] = LikedMovie.objects.filter(
            user=request.user, 
            movie=movie
        ).exists()
        watched_movie = WatchedMovie.objects.filter(
            user=request.user, 
            movie=movie
        ).first()
        response_data['status'] = '시청 중' if watched_movie else '미시청'

    # 장르 한글명 추가
    response_data['genres'] = [genre.name for genre in movie.genres.all()]
    
    return Response(response_data)


# 음성인식
# 음성 파일을 텍스트로 변환하는 함수
def transcribe_file(audio_file: str) -> str:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # WebM OPUS 형식으로 변경
        sample_rate_hertz=48000,  # 48000Hz로 변경
        language_code="ko",
        enable_automatic_punctuation=True,  # 자동 문장부호 추가
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript

# 감정 분석 함수
def sample_analyze_sentiment(text_content: str):
    client = language_v2.LanguageServiceClient()
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT
    language_code = "ko"

    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    encoding_type = language_v2.EncodingType.UTF8
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )

    sentiment_score = response.document_sentiment.score
    sentiment_magnitude = response.document_sentiment.magnitude
    return sentiment_score, sentiment_magnitude

# TMDB API 호출 함수
def search_movies(query: str):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_voice(request):
    try:
        if 'audio_file' not in request.FILES:
            return JsonResponse({"error": "오디오 파일이 없습니다."}, status=400)

        # 오디오 파일을 임시로 저장
        audio_path = "audio.wav"
        with open(audio_path, "wb") as f:
            for chunk in request.FILES["audio_file"].chunks():
                f.write(chunk)

        # 음성을 텍스트로 변환
        transcript = transcribe_file(audio_path)
        print(transcript)

        # 텍스트에 대해 감정 분석 수행
        sentiment_score, sentiment_magnitude = sample_analyze_sentiment(transcript)

        # 감정 점수에 따른 장르 ID 매핑
        if sentiment_score >= 0.3:  # 긍정적인 감정
            target_genres = [35, 12, 10751]  # 코미디(35), 모험(12), 가족(10751)
        elif sentiment_score <= -0.3:  # 부정적인 감정
            target_genres = [27, 53, 80]  # 공포(27), 스릴러(53), 범죄(80)
        else:  # 중립적인 감정
            target_genres = [18, 10749, 878]  # 드라마(18), 로맨스(10749), SF(878)

        # JSON 파일 경로
        json_path = Path(__file__).parent / 'fixtures' / 'genre_secure_movie_data.json'
        
        # JSON 파일 읽기
        with open(json_path, 'r', encoding='utf-8') as f:
            movies_data = json.load(f)

        # 장르에 맞는 영화 필터링
        filtered_movies = []
        for movie in movies_data:
            movie_genres = movie['fields']['genres']
            if any(genre in movie_genres for genre in target_genres):
                filtered_movies.append({
                    'id': movie['pk'],
                    'title': movie['fields']['title'],
                    'overview': movie['fields']['overview'],
                    'poster_path': movie['fields']['poster_path'],
                    'vote_avg': movie['fields']['vote_avg'],
                })

        # 중복 제거 및 랜덤 선택 (최대 5개)
        selected_movies = random.sample(filtered_movies, min(10, len(filtered_movies)))

        return JsonResponse({
            "transcript": transcript,
            "sentiment_score": sentiment_score,
            "sentiment_magnitude": sentiment_magnitude,
            "movies": selected_movies,
        })

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
    

# 리뷰 목록 생성 및 조회
@api_view(['GET', 'POST'])
def review_list_create(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movie_id')
        if movie_id:
            reviews = Review.objects.filter(movie_id=movie_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=401)
            
            # movie_id를 사용하여 Movie 객체 가져오기
            movie_id = request.data.get('movie_id')
            movie = get_object_or_404(Movie, pk=movie_id)
            
            # 필수 필드만 포함
            review_data = {
                'content': request.data.get('content'),
                'is_spoiler': request.data.get('is_spoiler', False),  # 기본값 False
                'movie': movie.id # movie 객체의 id를 저장
            }
            
            serializer = ReviewSerializer(data=review_data)
            if serializer.is_valid():
                review = serializer.save(user=request.user)  # user 정보 추가
                return Response(serializer.data, status=201)
            
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            print("Error creating review:", str(e))
            return Response({'error': str(e)}, status=500)


# 리뷰 상세 조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    
    if request.method == 'GET':
        # GET 요청은 인증 불필요
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    # PUT과 DELETE 요청은 인증 필요
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)


# 리뷰 좋아요 버튼
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    
    # 자신의 리뷰는 좋아요 할 수 없음
    if review.user == request.user:
        return Response({'error': '자신의 리뷰는 좋아요할 수 없습니다.'}, status=400)
    
    like_instance = LikedReview.objects.filter(user=request.user, review=review)
    
    if like_instance.exists():
        like_instance.delete()
        review.likes -= 1
        is_liked = False
    else:
        LikedReview.objects.create(user=request.user, review=review)
        review.likes += 1
        is_liked = True
    
    review.save()
    return Response({
        'likes': review.likes,
        'is_liked': is_liked
    })

@api_view(['GET'])
def search_movies_by_title(request):
    query = request.GET.get('query', '')
    if not query:
        return Response({'error': '검색어를 입력해주세요.'}, status=400)
    
    # 제목에 검색어가 포함된 영화들을 검색
    movies = Movie.objects.filter(title__icontains=query)[:10]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# 사용자가 작성한 리뷰 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    """사용자가 작성한 리뷰 목록을 반환"""
    try:
        reviews = Review.objects.filter(user=request.user)\
            .select_related('user', 'movie')\
            .prefetch_related(
                Prefetch(
                    'liked_by',
                    queryset=LikedReview.objects.filter(user=request.user),
                    to_attr='user_likes'
                )
            )\
            .order_by('-created_at')
        
        serializer = ReviewSerializer(
            reviews, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=500
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_reviews(request):
    """사용자가 좋아요한 리뷰 목록을 반환"""
    try:
        liked_reviews = Review.objects.filter(
            likedreview__user=request.user
        ).select_related('user', 'movie')\
         .prefetch_related('likedreview_set')\
         .order_by('-likedreview__created_at')
        
        serializer = ReviewSerializer(
            liked_reviews, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=500
        )


# 사용자가 좋아요한 리뷰 목록
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reviews(request):
    """사용자가 작성한 리뷰 목록을 반환"""
    try:
        reviews = Review.objects.filter(user=request.user)\
            .select_related('user', 'movie')\
            .prefetch_related(
                Prefetch(
                    'liked_by',
                    queryset=LikedReview.objects.filter(user=request.user),
                    to_attr='user_likes'
                )
            )\
            .order_by('-created_at')
        
        serializer = ReviewSerializer(
            reviews, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=500
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_reviews(request):
    """사용자가 좋아요한 리뷰 목록을 반환"""
    try:
        liked_reviews = Review.objects.filter(
            liked_by__user=request.user
        ).select_related('user', 'movie')\
         .prefetch_related(
            Prefetch(
                'liked_by',
                queryset=LikedReview.objects.filter(user=request.user),
                to_attr='user_likes'
            )
         )\
         .order_by('-liked_by__created_at')
        
        serializer = ReviewSerializer(
            liked_reviews, 
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=500
        )