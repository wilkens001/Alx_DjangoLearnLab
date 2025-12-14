"""
Tests for the posts app.

This module contains test cases for Post and Comment functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Post, Comment

User = get_user_model()


class PostModelTestCase(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
    
    def test_post_creation(self):
        """Test that posts are created correctly."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)
    
    def test_post_str(self):
        """Test post string representation."""
        expected = f"Test Post by {self.user.username}"
        self.assertEqual(str(self.post), expected)


class CommentModelTestCase(TestCase):
    """Test cases for Comment model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_comment_creation(self):
        """Test that comments are created correctly."""
        self.assertEqual(self.comment.content, 'Test comment')
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)


class PostAPITestCase(APITestCase):
    """Test cases for Post API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
    
    def test_list_posts(self):
        """Test retrieving list of posts."""
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_post(self):
        """Test creating a new post."""
        data = {
            'title': 'New Post',
            'content': 'New content'
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
    
    def test_retrieve_post(self):
        """Test retrieving a single post."""
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
    
    def test_update_post(self):
        """Test updating a post."""
        data = {
            'title': 'Updated Post',
            'content': 'Updated content'
        }
        response = self.client.put(f'/api/posts/{self.post.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')
    
    def test_delete_post(self):
        """Test deleting a post."""
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_create_post_unauthenticated(self):
        """Test that unauthenticated users cannot create posts."""
        self.client.credentials()  # Remove authentication
        data = {
            'title': 'Unauthorized Post',
            'content': 'Should fail'
        }
        response = self.client.post('/api/posts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentAPITestCase(APITestCase):
    """Test cases for Comment API endpoints."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.post = Post.objects.create(
            author=self.user,
            title='Test Post',
            content='Test content'
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content='Test comment'
        )
    
    def test_list_comments(self):
        """Test retrieving list of comments."""
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_comment(self):
        """Test creating a new comment."""
        data = {
            'post': self.post.id,
            'content': 'New comment'
        }
        response = self.client.post('/api/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
    
    def test_update_comment(self):
        """Test updating a comment."""
        data = {
            'post': self.post.id,
            'content': 'Updated comment'
        }
        response = self.client.put(f'/api/comments/{self.comment.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment')
    
    def test_delete_comment(self):
        """Test deleting a comment."""
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
