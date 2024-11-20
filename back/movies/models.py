from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.TextField(blank=True, null=True)
    released_date = models.DateField()
    runtime = models.IntegerField()
    popularity = models.FloatField(blank=True, null=True)
    vote_avg = models.FloatField(blank=True, null=True)

