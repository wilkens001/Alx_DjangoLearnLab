"""
Tests for the accounts app.

This module contains test cases for user authentication and profile management.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationTestCase(APITestCase):
    """Test cases for user registration."""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/register/'
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'bio': 'Test user bio'
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_registration_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
        }
        
        response = self.client.post(self.register_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTestCase(APITestCase):
    """Test cases for user login."""
    
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/login/'
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_login_success(self):
        """Test successful user login."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test login fails with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserFollowTestCase(APITestCase):
    """Test cases for user follow functionality."""
    
    def setUp(self):
        """Set up test users and authentication."""
        self.client = APIClient()
        
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        
        # Authenticate user1
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_follow_user_success(self):
        """Test successfully following another user."""
        url = f'/api/follow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())
    
    def test_cannot_follow_self(self):
        """Test that a user cannot follow themselves."""
        url = f'/api/follow/{self.user1.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_cannot_follow_already_followed_user(self):
        """Test that a user cannot follow someone they already follow."""
        # First follow
        self.user1.following.add(self.user2)
        
        # Try to follow again
        url = f'/api/follow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_follow_nonexistent_user(self):
        """Test following a user that doesn't exist."""
        url = '/api/follow/99999/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_unfollow_user_success(self):
        """Test successfully unfollowing a user."""
        # First follow the user
        self.user1.following.add(self.user2)
        
        # Now unfollow
        url = f'/api/unfollow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertFalse(self.user1.following.filter(id=self.user2.id).exists())
    
    def test_cannot_unfollow_not_followed_user(self):
        """Test that a user cannot unfollow someone they don't follow."""
        url = f'/api/unfollow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_follow_requires_authentication(self):
        """Test that following requires authentication."""
        # Remove authentication
        self.client.credentials()
        
        url = f'/api/follow/{self.user2.id}/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_followers_and_following_counts(self):
        """Test that followers and following counts are correct."""
        # user1 follows user2 and user3
        self.user1.following.add(self.user2, self.user3)
        
        # user2 follows user1
        self.user2.following.add(self.user1)
        
        self.assertEqual(self.user1.following_count, 2)
        self.assertEqual(self.user1.followers_count, 1)
        self.assertEqual(self.user2.followers_count, 1)
        self.assertEqual(self.user2.following_count, 1)
