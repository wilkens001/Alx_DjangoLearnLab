"""
URL configuration for the accounts app.

This module defines URL patterns for user authentication and profile management.
"""

from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserListView,
    UserDetailView,
    follow_user,
    unfollow_user
)

app_name = 'accounts'

urlpatterns = [
    # User registration endpoint
    # POST /api/register/
    path('register/', UserRegistrationView.as_view(), name='register'),
    
    # User login endpoint
    # POST /api/login/
    path('login/', UserLoginView.as_view(), name='login'),
    
    # User profile endpoint (requires authentication)
    # GET /api/profile/ - Retrieve profile
    # PUT/PATCH /api/profile/ - Update profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # List all users
    # GET /api/users/
    path('users/', UserListView.as_view(), name='user-list'),
    
    # User detail endpoint
    # GET /api/users/<int:pk>/
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # Follow user endpoint (requires authentication)
    # POST /api/follow/<int:user_id>/
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    
    # Unfollow user endpoint (requires authentication)
    # POST /api/unfollow/<int:user_id>/
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
]
