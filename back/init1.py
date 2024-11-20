import requests
import json
import os
import environ

# 환경변수 설정
env = environ.Env(DEBUG=(bool, True))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
TMDB_API_KEY = env('VITE_TMDB_API_KEY')

def get_movie_datas():
    total_data = []

    for i in range(1, 10):
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        try:
            response = requests.get(request_url)
            response.raise_for_status()
            movies = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching movie data on page {i}: {e}")
            continue

        for movie in movies.get('results', []):
            movie_id = movie['id']
            release_date_data = get_release_dates(movie_id)

            # 한국 기준 18세 미만인 영화만 추가
            if release_date_data and release_date_data['certification'] and int(release_date_data['certification']) < 18:
                fields = {
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids']
                }

                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)

    with open("movies/fixtures/secure_movie_data.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)


def get_release_dates(movie_id):
    """
    특정 영화의 release_dates API에서 한국(KR) 기준 18세 미만 등급 정보를 반환.
    """
    request_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(request_url)
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




get_movie_datas()