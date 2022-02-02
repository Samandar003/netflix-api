from email.policy import default
from django.test import TestCase, Client
from filmapp.serializers import MovieSerializers, ActorSerializers, CommentSerializer
from filmapp.models import Movie, Actor, Comment


class TestMovieViewSet(TestCase):
  def setUp(self) -> None:
    self.actor1 = Actor.objects.create(name='Tayson', birthdate='1975-10-02', gender=default)
    self.movie1 = Movie.objects.create(movie_name='New', imdb=45, year='2010-10-12')
  def test_data(self):
    data = MovieSerializers(self.movie1).data
    assert data['id'] is not None
    assert data['movie_name'] == 'New'
    assert data['imdb'] == 45
    assert data['year'] == '2010-10-12'
  
  def test_is_valid(self):
    data = {
      'movie_name':'Example movie',
      'year':'2010-01-02',
      'imdb':65,
      'genre':'C',
      'actors':self.actor1
    }
    serializer = MovieSerializers(data=data)
    # print(serializer.data)
    # serializer.save()
    self.assertTrue(serializer.is_valid(raise_exception=True))
     
     