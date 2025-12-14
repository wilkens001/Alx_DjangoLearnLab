"""
Custom User Model for Social Media API

This module defines a custom user model that extends Django's AbstractUser.
It includes additional fields for social media functionality:
- bio: A text field for user biography
- profile_picture: An image field for user profile pictures
- followers: A many-to-many relationship for following other users
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Attributes:
        bio (TextField): User's biography or description
        profile_picture (ImageField): User's profile picture
        followers (ManyToManyField): Users who follow this user
    """
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="User biography (max 500 characters)"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text="User profile picture"
    )
    
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="Users who follow this user"
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        """Return the number of followers."""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the number of users this user follows."""
        return self.following.count()
