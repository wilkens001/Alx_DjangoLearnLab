"""
Models for Posts and Comments in the Social Media API.

This module defines the Post and Comment models with relationships
to users and appropriate fields for content management.
"""

from django.db import models
from django.contrib.auth import get_user_model

# Example usage: models.TextField() for large text content
User = get_user_model()


class Post(models.Model):
    """
    Post model representing user-generated content.
    
    Attributes:
        author (ForeignKey): The user who created the post
        title (CharField): Post title
        content (TextField): Post content/body
        created_at (DateTimeField): Timestamp when post was created
        updated_at (DateTimeField): Timestamp when post was last updated
    """
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="User who created this post"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Post title (max 200 characters)"
    )
    
    content = models.TextField(
        help_text="Main content of the post"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when post was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when post was last updated"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    @property
    def comment_count(self):
        """Return the number of comments on this post."""
        return self.comments.count()


class Comment(models.Model):
    """
    Comment model representing user comments on posts.
    
    Attributes:
        post (ForeignKey): The post this comment belongs to
        author (ForeignKey): The user who created the comment
        content (TextField): Comment content
        created_at (DateTimeField): Timestamp when comment was created
        updated_at (DateTimeField): Timestamp when comment was last updated
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="Post this comment belongs to"
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="User who created this comment"
    )
    
    content = models.TextField(
        help_text="Comment content"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when comment was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when comment was last updated"
    )
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
