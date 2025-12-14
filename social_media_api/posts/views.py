"""
Views for the posts app.

This module defines viewsets for Post and Comment models with CRUD operations,
permissions, pagination, and filtering capabilities.
"""

from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, PostListSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model providing CRUD operations.
    
    List, create, retrieve, update, and delete posts.
    Includes filtering, searching, and ordering capabilities.
    
    Permissions:
        - List/Retrieve: Available to all authenticated users
        - Create: Authenticated users only
        - Update/Delete: Only the post author
    """
    
    queryset = Post.objects.all().select_related('author').prefetch_related('comments')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = ['author', 'author__username']
    
    # Search options
    search_fields = ['title', 'content']
    
    # Ordering options
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """
        Set the post author to the current authenticated user.
        """
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action to retrieve all comments for a specific post.
        
        GET /api/posts/{id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model providing CRUD operations.
    
    List, create, retrieve, update, and delete comments.
    
    Permissions:
        - List/Retrieve: Available to all authenticated users
        - Create: Authenticated users only
        - Update/Delete: Only the comment author
    """
    
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # Filtering options
    filterset_fields = ['post', 'author', 'author__username']
    
    # Ordering options
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']
    
    def perform_create(self, serializer):
        """
        Set the comment author to the current authenticated user.
        """
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        """
        Optionally filter comments by post_id from query parameters.
        """
        queryset = super().get_queryset()
        post_id = self.request.query_params.get('post', None)
        
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        
        return queryset
