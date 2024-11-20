from django.http import JsonResponse
from .models import Movie

def get_movies(request):
    TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'
    
    movies = Movie.objects.all()
    movies_data = []
    
    for movie in movies:
        movie_data = {
            'id': movie.id,
            'title': movie.title,
            'poster_path': f"{TMDB_IMAGE_BASE_URL}{movie.poster_path}" if movie.poster_path else None
        }
        movies_data.append(movie_data)
    
    return JsonResponse({'movies': movies_data})