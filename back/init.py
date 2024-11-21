import requests
import json

# API 키 환경변수에서 읽어오기
import os
import environ
# 환경변수를 불러올 수 있는 상태로 설정
env = environ.Env(DEBUG=(bool, True))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 읽어올 환경 변수 파일을 지정
environ.Env.read_env(env_file = os.path.join(BASE_DIR, '.env'))
TMDB_API_KEY = env('VITE_TMDB_API_KEY')

def get_movie_datas():
    total_data = []

    for i in range(1, 30):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        try:
            response = requests.get(request_url)
            response.raise_for_status()
            movies = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data on page {i}: {e}")
            continue

        for movie in movies.get('results', []):
            if movie.get('release_date', ''):
                movie_details = get_movie_details(movie['id'])
                fields = {
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'backdrop_path': movie['backdrop_path'],
                    'runtime': movie_details.get('runtime'),  # 추가된 필드
                    'genres': movie['genre_ids']
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("movies/fixtures/genre_unsecure_movie_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)

def get_movie_details(movie_id):
    """
    특정 영화의 상세 정보를 가져옵니다.
    """
    request_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR"
    try:
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details for movie ID {movie_id}: {e}")
        return {}



def get_genre_data():
    total_data = []

    request_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    genres = requests.get(request_url).json()

    for genre in genres['genres']:
        fields = {
            # 'genre_id': genre['id'],
            'name': genre['name'],
        }

        data = {
            "pk": genre['id'],
            "model": "movies.genre",
            "fields": fields
        }
        total_data.append(data)

    with open("movies/fixtures/genre_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)


get_movie_datas()
# get_genre_data()

'''
movies/fixtures/ 만들고 

python init.py 

python manage.py migrate

python manage.py loaddata genre_data.json movie_data.json

'''