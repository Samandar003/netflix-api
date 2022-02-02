from django.db import models
from django.contrib.auth import get_user_model
from datetime import date


class Actor(models.Model):
  GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
  ]
  name = models.CharField(max_length=50, blank=False, null=False)
  birthdate = models.DateField(max_length=20, blank=True)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='OTHER')
  
  def __str__(self):
    return self.name
  
class Movie(models.Model):
  GENRE_CHOICES = [
    ('A', 'Action'),
    ('C', 'Comedy'),
    ('D', 'Drama'),
    ('F', 'Fantastic'),
    ('H', 'Horror'),
    ('M', 'Mystery'),
    ('R', 'Romance'),
    ('T', 'Thriller'),
    ('O', 'Other'),
  ]
  movie_name = models.CharField(max_length=550, blank=False)
  year = models.DateField(max_length=500, blank=False)
  imdb = models.IntegerField()
  genre = models.CharField(max_length=1, choices=GENRE_CHOICES, default='OTHER')
  actors = models.ManyToManyField(Actor, related_name='actors')

  def __str__(self):
    return self.movie_name

User = get_user_model()

class Comment(models.Model):
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comment')
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_user')
      text = models.TextField(max_length=500)
      created_date = models.DateField(default=date.today, blank=False)
      
      def __str__(self):
        return f"To {self.movie} by {self.user}"
      
      