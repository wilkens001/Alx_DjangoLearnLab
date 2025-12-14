# User Follows and Feed API Documentation

This document provides comprehensive documentation for the User Follow System and Feed functionality in the Social Media API.

## Table of Contents
1. [Overview](#overview)
2. [Model Changes](#model-changes)
3. [Follow Management Endpoints](#follow-management-endpoints)
4. [Feed Endpoint](#feed-endpoint)
5. [Usage Examples](#usage-examples)
6. [Testing Guide](#testing-guide)

---

## Overview

The Social Media API now includes user relationship management through a follow system and a personalized content feed. Users can:
- Follow other users to see their content
- Unfollow users they no longer want to see content from
- View a personalized feed of posts from users they follow

### Key Features
- **Symmetric Follow System**: Following is one-directional (like Twitter/X)
- **Real-time Feed Updates**: Feed automatically reflects following changes
- **Chronological Ordering**: Feed shows most recent posts first
- **Efficient Queries**: Uses select_related and prefetch_related for optimal performance

---

## Model Changes

### CustomUser Model

The `CustomUser` model includes a many-to-many relationship for managing follows:

```python
class CustomUser(AbstractUser):
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text="Users who follow this user"
    )
```

**Fields:**
- `followers`: Users who follow this user (many-to-many)
- `following`: Users that this user follows (reverse relation)

**Properties:**
- `followers_count`: Number of followers
- `following_count`: Number of users being followed

---

## Follow Management Endpoints

### 1. Follow a User

Follow another user to see their posts in your feed.

**Endpoint:** `POST /api/follow/<int:user_id>/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/follow/2/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "message": "You are now following user2",
    "user": {
        "id": 2,
        "username": "user2",
        "bio": "User bio text",
        "profile_picture": "/media/profile_pictures/user2.jpg",
        "followers_count": 5,
        "following_count": 3
    }
}
```

**Error Responses:**

**400 Bad Request** - Attempting to follow yourself:
```json
{
    "error": "You cannot follow yourself"
}
```

**400 Bad Request** - Already following:
```json
{
    "error": "You are already following user2"
}
```

**404 Not Found** - User doesn't exist:
```json
{
    "detail": "Not found."
}
```

**401 Unauthorized** - Not authenticated:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 2. Unfollow a User

Stop following a user and remove their posts from your feed.

**Endpoint:** `POST /api/unfollow/<int:user_id>/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/unfollow/2/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "message": "You have unfollowed user2",
    "user": {
        "id": 2,
        "username": "user2",
        "bio": "User bio text",
        "profile_picture": "/media/profile_pictures/user2.jpg",
        "followers_count": 4,
        "following_count": 3
    }
}
```

**Error Responses:**

**400 Bad Request** - Not following the user:
```json
{
    "error": "You are not following user2"
}
```

**404 Not Found** - User doesn't exist:
```json
{
    "detail": "Not found."
}
```

**401 Unauthorized** - Not authenticated:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Feed Endpoint

### Get Personalized Feed

Retrieve posts from users you follow, ordered chronologically (newest first).

**Endpoint:** `GET /api/feed/`

**Authentication:** Required (Token)

**Query Parameters:**
- `page`: Page number for pagination (optional, default: 1)

**Request:**
```http
GET /api/feed/?page=1 HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "count": 15,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "results": [
        {
            "id": 23,
            "author": {
                "id": 2,
                "username": "user2",
                "bio": "Tech enthusiast",
                "profile_picture": "/media/profile_pictures/user2.jpg"
            },
            "title": "Latest Post from User2",
            "content": "This is the most recent post content...",
            "created_at": "2025-12-14T18:30:00Z",
            "updated_at": "2025-12-14T18:30:00Z",
            "comment_count": 5,
            "comments": [
                {
                    "id": 45,
                    "author": {
                        "id": 3,
                        "username": "user3"
                    },
                    "content": "Great post!",
                    "created_at": "2025-12-14T18:35:00Z"
                }
            ]
        },
        {
            "id": 22,
            "author": {
                "id": 5,
                "username": "user5",
                "bio": "Content creator",
                "profile_picture": null
            },
            "title": "Another Post",
            "content": "More interesting content...",
            "created_at": "2025-12-14T17:45:00Z",
            "updated_at": "2025-12-14T17:45:00Z",
            "comment_count": 2,
            "comments": []
        }
    ]
}
```

**Empty Feed Response (200 OK):**

If you don't follow anyone or followed users haven't posted:
```json
{
    "count": 0,
    "next": null,
    "previous": null,
    "results": []
}
```

**Error Responses:**

**401 Unauthorized** - Not authenticated:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

## Usage Examples

### Example Workflow: Following Users and Viewing Feed

#### 1. Register and Login

```bash
# Register a new user
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "bio": "Hello, I am Alice!"
  }'

# Response includes token
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "bio": "Hello, I am Alice!"
  },
  "token": "abc123token456def",
  "message": "User registered successfully"
}
```

#### 2. Follow Multiple Users

```bash
# Follow user with ID 2
curl -X POST http://localhost:8000/api/follow/2/ \
  -H "Authorization: Token abc123token456def"

# Follow user with ID 3
curl -X POST http://localhost:8000/api/follow/3/ \
  -H "Authorization: Token abc123token456def"

# Follow user with ID 5
curl -X POST http://localhost:8000/api/follow/5/ \
  -H "Authorization: Token abc123token456def"
```

#### 3. View Your Personalized Feed

```bash
# Get your feed
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token abc123token456def"
```

#### 4. Unfollow a User

```bash
# Unfollow user with ID 3
curl -X POST http://localhost:8000/api/unfollow/3/ \
  -H "Authorization: Token abc123token456def"
```

#### 5. Check Updated Feed

```bash
# Feed will now only show posts from users 2 and 5
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token abc123token456def"
```

---

### Python Example using `requests`

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login to get token
login_response = requests.post(f"{BASE_URL}/login/", json={
    "username": "alice",
    "password": "securepass123"
})
token = login_response.json()["token"]
headers = {"Authorization": f"Token {token}"}

# Follow a user
follow_response = requests.post(
    f"{BASE_URL}/follow/2/",
    headers=headers
)
print(follow_response.json())
# Output: {"message": "You are now following user2", "user": {...}}

# Get personalized feed
feed_response = requests.get(f"{BASE_URL}/feed/", headers=headers)
posts = feed_response.json()["results"]

for post in posts:
    print(f"{post['author']['username']}: {post['title']}")
    print(f"  Posted: {post['created_at']}")
    print(f"  {post['comment_count']} comments")
    print()

# Unfollow a user
unfollow_response = requests.post(
    f"{BASE_URL}/unfollow/2/",
    headers=headers
)
print(unfollow_response.json())
# Output: {"message": "You have unfollowed user2", "user": {...}}
```

---

### JavaScript Example using `fetch`

```javascript
const BASE_URL = 'http://localhost:8000/api';
let authToken = '';

// Login
async function login(username, password) {
    const response = await fetch(`${BASE_URL}/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });
    const data = await response.json();
    authToken = data.token;
    return data;
}

// Follow a user
async function followUser(userId) {
    const response = await fetch(`${BASE_URL}/follow/${userId}/`, {
        method: 'POST',
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Get feed
async function getFeed(page = 1) {
    const response = await fetch(`${BASE_URL}/feed/?page=${page}`, {
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Unfollow a user
async function unfollowUser(userId) {
    const response = await fetch(`${BASE_URL}/unfollow/${userId}/`, {
        method: 'POST',
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Usage
(async () => {
    // Login
    await login('alice', 'securepass123');
    
    // Follow users
    await followUser(2);
    await followUser(3);
    
    // Get feed
    const feed = await getFeed();
    console.log(`Found ${feed.count} posts in feed`);
    
    // Unfollow a user
    await unfollowUser(3);
})();
```

---

## Testing Guide

### Running Tests

```bash
# Run all tests
python manage.py test

# Run only follow and feed tests
python manage.py test accounts.tests.UserFollowTestCase posts.tests.FeedTestCase

# Run with verbose output
python manage.py test --verbosity=2
```

### Test Coverage

The implementation includes comprehensive test coverage:

**Follow System Tests (10 tests):**
- ✅ Successfully follow a user
- ✅ Cannot follow yourself
- ✅ Cannot follow already followed user
- ✅ Follow non-existent user returns 404
- ✅ Successfully unfollow a user
- ✅ Cannot unfollow user you don't follow
- ✅ Follow requires authentication
- ✅ Followers and following counts are accurate

**Feed System Tests (7 tests):**
- ✅ Feed shows only followed users' posts
- ✅ Feed ordered by creation date (newest first)
- ✅ Feed empty when not following anyone
- ✅ Feed updates when following changes
- ✅ Feed requires authentication
- ✅ Feed includes complete post details

### Manual Testing with cURL

```bash
# 1. Register two users
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@test.com","password":"test123","password_confirm":"test123"}'

curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"carol","email":"carol@test.com","password":"test123","password_confirm":"test123"}'

# 2. Bob creates a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token bob_token_here" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bob Post","content":"Hello from Bob!"}'

# 3. Carol follows Bob
curl -X POST http://localhost:8000/api/follow/1/ \
  -H "Authorization: Token carol_token_here"

# 4. Carol checks her feed (should see Bob's post)
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token carol_token_here"

# 5. Carol unfollows Bob
curl -X POST http://localhost:8000/api/unfollow/1/ \
  -H "Authorization: Token carol_token_here"

# 6. Carol checks her feed again (should be empty)
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token carol_token_here"
```

---

## Key Features Summary

### Follow System
- ✅ One-directional follow relationships (asymmetric)
- ✅ Cannot follow yourself
- ✅ Cannot follow the same user twice
- ✅ Proper error handling for edge cases
- ✅ Returns updated user information after follow/unfollow
- ✅ Requires authentication

### Feed System
- ✅ Shows posts only from followed users
- ✅ Chronologically ordered (newest first)
- ✅ Includes complete post details with author info
- ✅ Supports pagination (10 posts per page)
- ✅ Efficient database queries (select_related, prefetch_related)
- ✅ Real-time updates based on following relationships
- ✅ Empty feed when not following anyone
- ✅ Requires authentication

---

## Database Relationships

```
┌─────────────┐         followers         ┌─────────────┐
│             │◄─────────────────────────┐│             │
│ CustomUser  │                          ││ CustomUser  │
│             │──────────────────────────┘│             │
└──────┬──────┘       following           └──────┬──────┘
       │                                          │
       │ author (FK)                              │ author (FK)
       │                                          │
       ▼                                          ▼
┌─────────────┐                          ┌─────────────┐
│    Post     │                          │    Post     │
│             │                          │             │
└─────────────┘                          └─────────────┘
```

- `followers`: Many-to-many self-relationship on CustomUser
- `following`: Reverse relation (related_name)
- `author`: Foreign key from Post to CustomUser

---

## Performance Considerations

### Optimizations Implemented

1. **Query Optimization:**
   ```python
   # Feed view uses select_related and prefetch_related
   Post.objects.filter(
       author__in=following_users
   ).select_related('author').prefetch_related('comments')
   ```

2. **Pagination:**
   - Default: 10 posts per page
   - Prevents loading too much data at once
   - Improves API response time

3. **Database Indexing:**
   - Posts indexed by `created_at` (for feed ordering)
   - User relationships use efficient many-to-many through table

### Best Practices

- Always authenticate requests with Token authentication
- Use pagination parameters for large feeds
- Cache follow relationships on client side when appropriate
- Limit the number of follows per user if needed (application logic)

---

## Troubleshooting

### Common Issues

**Issue:** "Authentication credentials were not provided"
- **Solution:** Include `Authorization: Token your_token` header in all requests

**Issue:** Cannot follow user - "You are already following this user"
- **Solution:** Check if you're already following the user before attempting to follow

**Issue:** Feed is empty
- **Solution:** Make sure you're following users and they have created posts

**Issue:** Old posts still appearing after unfollow
- **Solution:** This is expected - posts are loaded when you request the feed, not cached

---

## API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/follow/<user_id>/` | ✅ Yes | Follow a user |
| POST | `/api/unfollow/<user_id>/` | ✅ Yes | Unfollow a user |
| GET | `/api/feed/` | ✅ Yes | Get personalized feed |
| GET | `/api/profile/` | ✅ Yes | View your profile (includes followers/following) |
| GET | `/api/users/<id>/` | ❌ No | View any user's profile |

---

## Future Enhancements

Potential improvements for future versions:

1. **Follow Requests:** Add approval system for private accounts
2. **Block System:** Allow users to block others
3. **Feed Algorithms:** Implement engagement-based ranking
4. **Notifications:** Notify users when someone follows them
5. **Mutual Follows:** Endpoint to list mutual followers
6. **Follow Suggestions:** Recommend users to follow
7. **Activity Feed:** Show likes, comments, and follows in one feed

---

## Support

For issues or questions:
- Check the test cases in `accounts/tests.py` and `posts/tests.py`
- Review the view implementations in `accounts/views.py` and `posts/views.py`
- Ensure all migrations are applied: `python manage.py migrate`

---

**Last Updated:** December 14, 2025
**API Version:** 1.0
**Django Version:** 5.2.7
**DRF Version:** 3.15.2
