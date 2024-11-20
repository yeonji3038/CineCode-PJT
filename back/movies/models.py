from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    poster_path = models.TextField()
    released_date = models.DateField()
    runtime = models.IntegerField()

