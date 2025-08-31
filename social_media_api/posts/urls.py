from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.UserFeedView.as_view(), name='user_feed'),
]