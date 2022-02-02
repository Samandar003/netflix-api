from urllib import request
from django.db import reset_queries
from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import ActorSerializers, MovieSerializers, CommentSerializer
from .models import Actor, Movie, Comment
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import filters
from rest_framework.filters import OrderingFilter
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework import mixins


# class ActorAPIView(APIView):
#   def get(self, request):
#     actors = Actor.objects.all()
#     serializers = ActorSerializers(actors, many=True)
#     return Response(data=serializers.data)
#   def post(self, request):
#     serializer = ActorSerializers(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(data=serializer.data) 

class ActorViewSet(ModelViewSet):
  queryset = Actor.objects.all()
  serializer_class = ActorSerializers
  pagination_class = LimitOffsetPagination

# class MovieAPIView(APIView):
#   def get(self, request):
#     movies = Movie.objects.all()
#     serializers = MovieSerializers(movies, many=True)
#     return Response(data=serializers.data)

#   def post(self, request):
#     serializer = MovieSerializers(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(data=serializer.data)
  
# class MovieDetailAPIView(APIView):
#   def get(self, request, pk):
#     movies = Movie.objects.get(id=pk)
#     serializers = MovieSerializers(movies)
#     return Response(data=serializers.data)  
  
class MovieActorsAPIView(APIView):
  def get(self, request, pk):
    movie = Movie.objects.get(id=pk)
    serializer = ActorSerializers(movie.actors, many=True)
    return Response(serializer.data)
  
  
class MovieViewSet(ReadOnlyModelViewSet):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializers
  pagination_class = LimitOffsetPagination
  # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
  filter_backends = [filters.OrderingFilter, filters.SearchFilter]
  ordering_fields = ['imdb', '-imdb']
  search_fields = ['movie_name', 'genre']
  def get_queryset(self):
    queryset = Movie.objects.all()
    query = self.request.query_params.get('search')
    if query:
      queryset = Movie.objects.annotate(
        similarity=TrigramSimilarity('movie_name', query)
      ).filter(similarity__gt=0.5).order_by('-similarity')
    return queryset
 
  
  @action(detail=True, methods=['GET'])
  def actors(self, request, *args, **kwargs):
    movie = self.get_object()
    serializer = ActorSerializers(movie.actors, many=True)
    return Response(serializer.data)
  @action(detail=True, methods=['PUT'])
  def add_actor(self, request, *args, **kwargs):
      movie = self.get_object()
      actor = Actor.objects.get(id=request.data.get('id'))
      movie.actors.add(actor)
      return Response(status=status.HTTP_202_ACCEPTED)
      
  @action(detail=True, methods=['POST'])
  def remove_actor(self, request, *args, **kwargs):
      movie = self.get_object()
      id = request.data.get("id")
      print(id)
      actor = Actor.objects.get(id=id)
      serializer = ActorSerializers(actor)
      # print(actor.first_name)
      movie.actors.remove(actor)
      return Response(serializer.data)

 
# class CommentDetailAPIView(APIView):
#   def get(self, request, pk):
#       comments = Comment.objects.get(id=pk)
#       serializer = CommentSerializer(comments)
#       return Response(serializer.data)
      
# class CommentList(generics.ListAPIView):
#   queryset = Comment.objects.all()
#   serializer_class = CommentSerializer
#   authentication_classes = (TokenAuthentication,)
#   permission_classes = (IsAuthenticated,)

# class CommentDetail(generics.RetrieveAPIView):
#    queryset = Comment.objects.get()
#    serializer_class = CommentSerializer
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)

# class CommentCreate(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer 
#     permission_classes = [IsAuthenticated,]
#     authentication_classes = [TokenAuthentication,] 

class CommentViewSet(ModelViewSet):
  serializer_class = CommentSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
  

class CommentList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated,]
  
  def get(self, request, *args, **kwargs):
    return self.list(request, *args, **kwargs)
  def post(self, request, *args, **kwargs):
    return self.create(request, *args, **kwargs)

# class CommentCreateGetAPIView(APIView):
#   authentication_classes = [TokenAuthentication,]
#   permission_classes = [IsAuthenticated,]
#   def get(self, request):
#     comments = Comment.objects.filter(user=self.request.user)
#     serializer = CommentSerializer(comments, many=True)
#     return Response(serializer.data)
  
#   def post(self, request):
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  
class CommentAPIView(APIView):
  authentication_classes = [TokenAuthentication,]
  permission_classes = [IsAuthenticated,]
  def get(self, request, pk):
    comment = Comment.objects.get(id=pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
 
 
  def delete(self, request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  def post(self, request):
    comment = CommentSerializer(data=request.data)
    comment.is_valid(raise_exception=True)
    comment.save()
    return Response(status=status.HTTP_201_CREATED)
  

class CommentGet(generics.ListAPIView):
  serializer_class = CommentSerializer
  authentication_classes = (TokenAuthentication,)
  permission_classes = (IsAuthenticated,)
    
  def get_queryset(self):
    return Comment.objects.filter(user=self.request.user)
  
# class CommentCreate(generics.ListCreateAPIView):
#   authentication_classes = (TokenAuthentication,)
#   permission_classes = (IsAuthenticated,)
#   serializer_class = CommentSerializer
#   def get_queryset(self):
#     return Comment.objects.filter(user=self.request.user)
  
#   def perform_create(self, serializer):
#     serializer.save(owner=self.request.user)  




