import requests
import json
import os
import environ

# 환경변수 설정
env = environ.Env(DEBUG=(bool, True))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
TMDB_API_KEY = env('TMDB_ACCESS_TOKEN')

# TMDB API 헤더 설정
headers = {
    'Authorization': f'Bearer {TMDB_API_KEY}',
    'accept': 'application/json'
}

# 영화 데이터 가져오기
def get_movie_datas():
    total_data = []

    # 600개 불러옴
    for i in range(1, 90):
        request_url = f"https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}"
        try:
            response = requests.get(request_url, headers=headers)
            response.raise_for_status()
            movies = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data on page {i}: {e}")
            continue

        for movie in movies.get('results', []):
            movie_id = movie['id']
            release_date_data = get_release_dates(movie_id)
            movie_details = get_movie_details(movie_id)

            # 예고편 ID 가져오기
            trailer_id = get_youtube_trailer_id(movie['title'])

            # 한국 기준 18세 미만인 영화만 추가
            if release_date_data and release_date_data['certification'] and int(release_date_data['certification']) < 18:
                fields = {
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'runtime': movie_details.get('runtime'),  # 추가된 필드
                    'genres': movie['genre_ids'],
                    'trailer_id': trailer_id  # 추가
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("movies/fixtures/genre_secure_movie_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)


def get_movie_details(movie_id):
    """
    특정 영화의 상세 정보를 가져옵니다.
    """
    request_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko-KR"
    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details for movie ID {movie_id}: {e}")
        return {}


def get_release_dates(movie_id):
    """
    특정 영화의 release_dates API에서 한국(KR) 기준 18세 미만 등급 정보를 반환.
    """
    request_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        release_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching release dates for movie ID {movie_id}: {e}")
        return None

    # 한국(KR) 기준 release_dates에서 18세 미만 인증 필터링
    for result in release_data.get('results', []):
        if result['iso_3166_1'] == 'KR':
            for release in result.get('release_dates', []):
                if release['certification'] and release['certification'].isdigit() and int(release['certification']) < 18:
                    return release
    return None

def get_youtube_trailer_id(movie_title):
    """
    영화 제목으로 YouTube 예고편 검색
    """
    youtube_url = 'https://www.googleapis.com/youtube/v3/search'
    try:
        youtube_response = requests.get(youtube_url, params={
            'key': env('YOUTUBE_API_KEY'),
            'q': f'{movie_title} 예고편',
            'part': 'snippet',
            'maxResults': 1,
            'type': 'video'
        })
        youtube_data = youtube_response.json()
        if youtube_data.get('items'):
            return youtube_data['items'][0]['id']['videoId']
    except Exception as e:
        print(f"Error fetching YouTube trailer for {movie_title}: {e}")
    return None


get_movie_datas()