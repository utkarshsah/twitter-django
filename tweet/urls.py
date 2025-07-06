from.import views
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TweetViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)



urlpatterns = [
    path('', views.tweet_list,name='tweet_list'),
    path('create/', views.tweet_create,name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit,name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete,name='tweet_delete'),
    path('register/', views.register,name='register'),
    path('tweet/<int:tweet_id>/like/',views.like_tweet,name ='like_tweet'),

    path('', include(router.urls))
    ] 
 
