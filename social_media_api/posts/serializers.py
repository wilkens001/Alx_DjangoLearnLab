"""
Serializers for the posts app.

This module defines serializers for Post and Comment models,
handling data validation and representation.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    
    Includes author information and handles comment creation/updates.
    """
    
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    post_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'post_id', 'author', 'author_id', 
                  'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'author_id', 'post_id', 
                           'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create a new comment with the authenticated user as author.
        """
        # The author is set in the view from request.user
        return Comment.objects.create(**validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    
    Includes author information, comment count, and nested comments.
    """
    
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 
                  'created_at', 'updated_at', 'comment_count', 'comments']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 
                           'updated_at', 'comment_count']
    
    def create(self, validated_data):
        """
        Create a new post with the authenticated user as author.
        """
        # The author is set in the view from request.user
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update an existing post.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing posts without nested comments.
    """
    
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_id', 'title', 'content', 
                  'created_at', 'updated_at', 'comment_count']
        read_only_fields = ['id', 'author', 'author_id', 'created_at', 
                           'updated_at', 'comment_count']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    
    Handles like creation and displays user and post information.
    """
    
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    post_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_id', 'post', 'post_id', 'created_at']
        read_only_fields = ['id', 'user', 'user_id', 'post_id', 'created_at']
