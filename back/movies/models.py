from django.db import models
from django.conf import settings

class Movie(models.Model):
    STATUS_CHOICES = [
        ('미시청', '미시청'),
        ('시청 중', '시청 중'),
        ('시청 완료', '시청 완료'),
    ]

    title = models.CharField(max_length=200)
    poster_path = models.TextField(null=True, blank=True)
    released_date = models.DateField()
    runtime = models.IntegerField(null=True, blank=True)
    popularity = models.FloatField(null=True, blank=True)
    vote_avg = models.FloatField(null=True, blank=True)
    overview = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='미시청'
    )
    genres = models.ManyToManyField('Genre', through='MovieGenre')
    tags = models.ManyToManyField('Tag', through='MovieTag')
    watched_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='WatchedMovie',
        related_name='watched_movies'
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='LikedMovie',
        related_name='liked_movies'
    )

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TagCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_genres'

class MovieTag(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_tags'

class WatchedMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'watched_movies'

class LikedMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'liked_movies'
