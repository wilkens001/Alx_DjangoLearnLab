"""
Tests for the notifications app.

This module contains test cases for Notification functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Notification
from posts.models import Post

User = get_user_model()


class NotificationModelTestCase(TestCase):
    """Test cases for Notification model."""
    
    def setUp(self):
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
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='Test content'
        )
        self.notification = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(self.post),
            target_object_id=self.post.id
        )
    
    def test_notification_creation(self):
        """Test that notifications are created correctly."""
        self.assertEqual(self.notification.recipient, self.user1)
        self.assertEqual(self.notification.actor, self.user2)
        self.assertEqual(self.notification.verb, 'liked your post')
        self.assertFalse(self.notification.read)
    
    def test_notification_str(self):
        """Test notification string representation."""
        expected = f"user2 liked your post - user1"
        self.assertEqual(str(self.notification), expected)
    
    def test_mark_as_read(self):
        """Test marking notification as read."""
        self.assertFalse(self.notification.read)
        self.notification.mark_as_read()
        self.assertTrue(self.notification.read)


class NotificationAPITestCase(APITestCase):
    """Test cases for Notification API."""
    
    def setUp(self):
        """Set up test users and notifications."""
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
        
        # Create test post
        self.post = Post.objects.create(
            author=self.user1,
            title='Test Post',
            content='Test content'
        )
        
        # Create test notifications
        self.notification1 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(self.post),
            target_object_id=self.post.id
        )
        self.notification2 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='started following you',
            target_content_type=ContentType.objects.get_for_model(self.user2),
            target_object_id=self.user2.id,
            read=True
        )
        
        # Authenticate user1
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_list_notifications(self):
        """Test listing all notifications."""
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_list_unread_notifications(self):
        """Test listing only unread notifications."""
        response = self.client.get('/api/notifications/?unread=true')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.notification1.id)
    
    def test_mark_notification_as_read(self):
        """Test marking a specific notification as read."""
        url = f'/api/notifications/{self.notification1.id}/read/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify notification is now read
        self.notification1.refresh_from_db()
        self.assertTrue(self.notification1.read)
    
    def test_mark_all_notifications_as_read(self):
        """Test marking all notifications as read."""
        # Create another unread notification
        Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb='commented on your post',
            target_content_type=ContentType.objects.get_for_model(self.post),
            target_object_id=self.post.id
        )
        
        response = self.client.post('/api/notifications/mark-all-read/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify all notifications are now read
        unread_count = Notification.objects.filter(
            recipient=self.user1,
            read=False
        ).count()
        self.assertEqual(unread_count, 0)
    
    def test_notifications_require_authentication(self):
        """Test that notifications require authentication."""
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_only_sees_own_notifications(self):
        """Test that users only see their own notifications."""
        # Create notification for user2
        Notification.objects.create(
            recipient=self.user2,
            actor=self.user1,
            verb='liked your post'
        )
        
        response = self.client.get('/api/notifications/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should only see 2 notifications (both for user1)
        self.assertEqual(len(response.data), 2)
        for notification in response.data:
            self.assertEqual(notification['recipient'], 'user1')
    
    def test_cannot_mark_others_notification_read(self):
        """Test that users cannot mark other users' notifications as read."""
        # Create notification for user2
        notification = Notification.objects.create(
            recipient=self.user2,
            actor=self.user1,
            verb='liked your post'
        )
        
        url = f'/api/notifications/{notification.id}/read/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
