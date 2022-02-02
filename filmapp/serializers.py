import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Actor, Movie, Comment
from datetime import date


class ActorSerializers(serializers.ModelSerializer):
  class Meta:
    model = Actor
    fields = '__all__'
  def validate_birthdate(self, value):
    year = date(1950, 1, 1)
    if value<year:
      raise ValidationError(detail='Year must be greater than 1950')
    return value 
    
    
class MovieSerializers(serializers.ModelSerializer):
  # actors = ActorSerializers()
  class Meta:
    model = Movie
    fields = '__all__'
  def validate_genre(self, value):
    if value=='H':
      raise ValidationError(detail='Must not be Horror')
    return value
  def validate_year(self, value):
    year = date(2000, 10, 10)
    if value<year:
      raise ValidationError(detail='must be greater than 2000')
    return value

class CommentSerializer(serializers.ModelSerializer):
  # owner = serializers.ReadOnlyField(source='owner.username')
  class Meta:
    model = Comment
    fields = ('id', 'user', 'movie', 'text')
  
    