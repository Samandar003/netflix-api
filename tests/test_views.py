from django.test import TestCase, Client
from filmapp.serializers import MovieSerializers, ActorSerializers, CommentSerializer
from filmapp.models import Movie, Actor, Comment
from filmapp.views import MovieViewSet

class TestMovieViewSet(TestCase):
  def setUp(self) -> None:
    self.client = Client()
    self.actor1 = Actor.objects.create(name='Jekki', birthdate='1970-02-15')
    self.movie1 = Movie.objects.create(movie_name='Example1 film', imdb=75, year='2009-10-01')
    self.movie2 = Movie.objects.create(movie_name='Example2 film', imdb=71, year='2008-09-12')
  def test_get_all_movies(self):
    response = self.client.get('/movies/')
    self.assertEquals(response.status_code, 200)
    # print(response.data)
    data = response.data
    self.assertEquals(response.status_code, 200)
    self.assertEquals(len(data), 2)
    self.assertIsNotNone(data[0]['id'])
    self.assertEquals(data[0]['movie_name'], 'Example1 film')
  
  # def test_search(self):
  #   response = self.client.get('/movies/?search=Example1 film')
  #   # data = response.data 
  #   self.assertEquals(response.status_code, 200)  
  #   # self.assertEquals(len(data), 1)    
    # self.assertEquals(data[0]['movie_name'], 'Test Song')
    # self.assertEquals(data[0]['album'], self.album.id)
  
    
      
    