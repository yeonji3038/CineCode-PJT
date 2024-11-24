from django.db import models
from django.conf import settings
from movies.models import Movie

# 카테고리
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 태그
class Tag(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return self.name

# 사용자 영화 태그  
class UserMovieTag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie', 'tag')  # 동일한 사용자가 같은 영화에 같은 태그를 중복 적용하지 못하도록

    def __str__(self):
        return f"{self.user.username}의 {self.movie.title} - {self.tag.name}"