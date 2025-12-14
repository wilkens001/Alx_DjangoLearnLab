"""
Tests for the posts app.

This module contains test cases for Post and Comment functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Post, Comment, Like

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


class FeedTestCase(APITestCase):
    """Test cases for feed functionality."""
    
    def setUp(self):
        """Set up test users, follows, and posts."""
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
        self.user4 = User.objects.create_user(
            username='user4',
            email='user4@example.com',
            password='testpass123'
        )
        
        # user1 follows user2 and user3
        self.user1.following.add(self.user2, self.user3)
        
        # Create posts from different users
        self.post1 = Post.objects.create(
            author=self.user2,
            title='Post from User2',
            content='Content from user2'
        )
        self.post2 = Post.objects.create(
            author=self.user3,
            title='Post from User3',
            content='Content from user3'
        )
        self.post3 = Post.objects.create(
            author=self.user4,
            title='Post from User4',
            content='Content from user4 (not followed)'
        )
        self.post4 = Post.objects.create(
            author=self.user2,
            title='Another post from User2',
            content='More content from user2'
        )
        
        # Authenticate user1
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_feed_shows_followed_users_posts(self):
        """Test that feed shows posts from followed users only."""
        response = self.client.get('/api/feed/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Should have 3 posts (2 from user2, 1 from user3)
        self.assertEqual(len(response.data['results']), 3)
        
        # Check that posts are from followed users
        post_authors = [post['author']['username'] for post in response.data['results']]
        self.assertIn('user2', post_authors)
        self.assertIn('user3', post_authors)
        self.assertNotIn('user4', post_authors)
    
    def test_feed_ordered_by_creation_date(self):
        """Test that feed posts are ordered by creation date (newest first)."""
        response = self.client.get('/api/feed/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get the posts in order
        posts = response.data['results']
        
        # post4 should be first (most recent from user2)
        self.assertEqual(posts[0]['title'], 'Another post from User2')
        
        # Verify posts are in descending order by created_at
        for i in range(len(posts) - 1):
            self.assertGreaterEqual(posts[i]['created_at'], posts[i + 1]['created_at'])
    
    def test_feed_empty_when_not_following_anyone(self):
        """Test that feed is empty when user doesn't follow anyone."""
        # Authenticate as user4 who doesn't follow anyone
        token4 = Token.objects.create(user=self.user4)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token4.key}')
        
        response = self.client.get('/api/feed/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    
    def test_feed_updates_when_following_changes(self):
        """Test that feed updates when user follows/unfollows someone."""
        # Initial feed has 3 posts
        response = self.client.get('/api/feed/')
        self.assertEqual(len(response.data['results']), 3)
        
        # user1 follows user4
        self.user1.following.add(self.user4)
        
        # Feed should now have 4 posts
        response = self.client.get('/api/feed/')
        self.assertEqual(len(response.data['results']), 4)
        
        # user1 unfollows user2
        self.user1.following.remove(self.user2)
        
        # Feed should now have 2 posts (1 from user3, 1 from user4)
        response = self.client.get('/api/feed/')
        self.assertEqual(len(response.data['results']), 2)
    
    def test_feed_requires_authentication(self):
        """Test that feed requires authentication."""
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get('/api/feed/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_feed_includes_post_details(self):
        """Test that feed includes complete post details."""
        response = self.client.get('/api/feed/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that posts have all expected fields
        post = response.data['results'][0]
        self.assertIn('id', post)
        self.assertIn('author', post)
        self.assertIn('title', post)
        self.assertIn('content', post)
        self.assertIn('created_at', post)
        self.assertIn('updated_at', post)
        self.assertIn('comments', post)


class LikeTestCase(APITestCase):
    """Test cases for like functionality."""
    
    def setUp(self):
        """Set up test users and posts."""
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
        
        # Create test posts
        self.post1 = Post.objects.create(
            author=self.user1,
            title='Post 1',
            content='Content 1'
        )
        self.post2 = Post.objects.create(
            author=self.user2,
            title='Post 2',
            content='Content 2'
        )
        
        # Authenticate user1
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
    
    def test_like_post_success(self):
        """Test successfully liking a post."""
        url = f'/api/posts/{self.post2.id}/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertTrue(Like.objects.filter(user=self.user1, post=self.post2).exists())
    
    def test_cannot_like_post_twice(self):
        """Test that a user cannot like the same post twice."""
        # First like
        Like.objects.create(user=self.user1, post=self.post2)
        
        # Try to like again
        url = f'/api/posts/{self.post2.id}/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_unlike_post_success(self):
        """Test successfully unliking a post."""
        # First like the post
        Like.objects.create(user=self.user1, post=self.post2)
        
        # Now unlike
        url = f'/api/posts/{self.post2.id}/unlike/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertFalse(Like.objects.filter(user=self.user1, post=self.post2).exists())
    
    def test_cannot_unlike_not_liked_post(self):
        """Test that a user cannot unlike a post they haven't liked."""
        url = f'/api/posts/{self.post2.id}/unlike/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_like_nonexistent_post(self):
        """Test liking a post that doesn't exist."""
        url = '/api/posts/99999/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_like_requires_authentication(self):
        """Test that liking requires authentication."""
        # Remove authentication
        self.client.credentials()
        
        url = f'/api/posts/{self.post2.id}/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_like_creates_notification(self):
        """Test that liking a post creates a notification for the post author."""
        from notifications.models import Notification
        
        url = f'/api/posts/{self.post2.id}/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check notification was created
        notification = Notification.objects.filter(
            recipient=self.post2.author,
            actor=self.user1,
            verb='liked your post'
        ).first()
        
        self.assertIsNotNone(notification)
        self.assertFalse(notification.read)
    
    def test_like_own_post_no_notification(self):
        """Test that liking own post doesn't create a notification."""
        from notifications.models import Notification
        
        url = f'/api/posts/{self.post1.id}/like/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check no notification was created
        notification_count = Notification.objects.filter(
            recipient=self.user1,
            actor=self.user1
        ).count()
        
        self.assertEqual(notification_count, 0)
