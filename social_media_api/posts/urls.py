"""
URL configuration for the posts app.

This module defines URL patterns for posts and comments using DRF routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, like_post, unlike_post

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

app_name = 'posts'

urlpatterns = [
    # Feed endpoint - must come before router URLs to avoid conflicts
    # Add a route in posts/urls.py for the feed endpoint, such as /feed/
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Like and unlike endpoints
    # POST /api/posts/<int:pk>/like/ and /posts/<int:pk>/unlike/
    path('posts/<int:pk>/like/', like_post, name='like-post'),
    
    # POST /api/posts/<int:pk>/unlike/
    path('posts/<int:pk>/unlike/', unlike_post, name='unlike-post'),
    
    # Include all router URLs
    path('', include(router.urls)),
]
