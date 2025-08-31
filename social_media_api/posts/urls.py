from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.UserFeedView.as_view(), name='user_feed'),
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    path('posts/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]
]