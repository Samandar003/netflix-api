
from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import views
from rest_framework.authtoken.views import obtain_auth_token
from .views import ActorViewSet, MovieViewSet, CommentViewSet, CommentList, CommentAPIView, CommentGet
# from .views import MovieAPIView
from .views import MovieActorsAPIView
# MovieDetailAPIView
# from .views import MovieViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('actors', ActorViewSet),
router.register('movies', MovieViewSet),
# router.register('comments', CommentViewSet, basename='comments'),


urlpatterns = [
    path('', include(router.urls)),
    # path('movies/', MovieAPIView.as_view(), name='movie-actors'),
    # path('movies/<int:pk>/', MovieDetailAPIView.as_view()),
    path('movies/<int:pk>/actors', MovieActorsAPIView.as_view(), name='movie_detail_actors'),
    path('comments/<int:pk>/', CommentAPIView.as_view(), name='comments_detail'),
    path('comments/', CommentAPIView.as_view(), name='comments'),
    path('comments_list/', CommentGet.as_view(), name='comments_list'),
    # path('cmments_new/', CommentCreate.as_view())
]

