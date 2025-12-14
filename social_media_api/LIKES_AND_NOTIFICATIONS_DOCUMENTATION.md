# Likes and Notifications API Documentation

Comprehensive documentation for the Likes and Notifications functionality in the Social Media API (Task 3).

## Table of Contents
1. [Overview](#overview)
2. [Model Definitions](#model-definitions)
3. [Like Endpoints](#like-endpoints)
4. [Notification Endpoints](#notification-endpoints)
5. [Usage Examples](#usage-examples)
6. [Testing Guide](#testing-guide)

---

## Overview

The Social Media API now includes likes and notifications systems to enhance user engagement:

### Likes System
- Users can like and unlike posts
- Prevents duplicate likes (unique constraint)
- Creates notifications for post authors
- Tracks like timestamps

### Notifications System
- Notifications for likes, comments, and follows
- Unread/read status tracking
- Filter by unread notifications
- Mark individual or all notifications as read
- GenericForeignKey for flexible target objects

---

## Model Definitions

### Like Model

Located in `posts/models.py`:

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # Prevents duplicate likes
```

**Fields:**
- `user`: User who liked the post (ForeignKey)
- `post`: Post that was liked (ForeignKey)
- `created_at`: Timestamp when like was created

**Constraints:**
- Unique together on (user, post) prevents multiple likes from same user

---

### Notification Model

Located in `notifications/models.py`:

```python
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
```

**Fields:**
- `recipient`: User receiving the notification
- `actor`: User who performed the action
- `verb`: Description of the action (e.g., "liked your post")
- `target`: GenericForeignKey to any object type
- `timestamp`: When notification was created
- `read`: Whether notification has been read

---

## Like Endpoints

### 1. Like a Post

Like a specific post.

**Endpoint:** `POST /api/posts/<int:pk>/like/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/posts/5/like/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (201 Created):**
```json
{
    "message": "You liked the post \"Amazing Post Title\"",
    "like": {
        "id": 12,
        "user": "username",
        "user_id": 3,
        "post": 5,
        "post_id": 5,
        "created_at": "2025-12-14T20:30:00Z"
    }
}
```

**Error Responses:**

**400 Bad Request** - Already liked:
```json
{
    "error": "You have already liked this post"
}
```

**404 Not Found** - Post doesn't exist:
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

**Side Effects:**
- Creates a Like object
- Creates a Notification for post author (if not liking own post)

---

### 2. Unlike a Post

Remove a like from a post.

**Endpoint:** `POST /api/posts/<int:pk>/unlike/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/posts/5/unlike/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "message": "You unliked the post \"Amazing Post Title\""
}
```

**Error Responses:**

**400 Bad Request** - Post not liked:
```json
{
    "error": "You have not liked this post"
}
```

**404 Not Found** - Post doesn't exist:
```json
{
    "detail": "Not found."
}
```

---

## Notification Endpoints

### 1. List Notifications

Retrieve all notifications for the authenticated user.

**Endpoint:** `GET /api/notifications/`

**Authentication:** Required (Token)

**Query Parameters:**
- `unread` (optional): Filter for unread notifications only (`true` or `false`)

**Request:**
```http
GET /api/notifications/?unread=true HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
[
    {
        "id": 15,
        "recipient": "alice",
        "recipient_id": 1,
        "actor": "bob",
        "actor_id": 2,
        "verb": "liked your post",
        "target_type": "post",
        "target_id": 5,
        "timestamp": "2025-12-14T20:30:00Z",
        "read": false
    },
    {
        "id": 14,
        "recipient": "alice",
        "recipient_id": 1,
        "actor": "carol",
        "actor_id": 3,
        "verb": "started following you",
        "target_type": "customuser",
        "target_id": 1,
        "timestamp": "2025-12-14T19:15:00Z",
        "read": false
    },
    {
        "id": 13,
        "recipient": "alice",
        "recipient_id": 1,
        "actor": "bob",
        "actor_id": 2,
        "verb": "commented on your post",
        "target_type": "post",
        "target_id": 3,
        "timestamp": "2025-12-14T18:45:00Z",
        "read": true
    }
]
```

**Error Responses:**

**401 Unauthorized** - Not authenticated:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

---

### 2. Mark Notification as Read

Mark a specific notification as read.

**Endpoint:** `POST /api/notifications/<int:pk>/read/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/notifications/15/read/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "message": "Notification marked as read",
    "notification": {
        "id": 15,
        "recipient": "alice",
        "recipient_id": 1,
        "actor": "bob",
        "actor_id": 2,
        "verb": "liked your post",
        "target_type": "post",
        "target_id": 5,
        "timestamp": "2025-12-14T20:30:00Z",
        "read": true
    }
}
```

**Error Responses:**

**404 Not Found** - Notification doesn't exist or doesn't belong to user:
```json
{
    "detail": "Not found."
}
```

---

### 3. Mark All Notifications as Read

Mark all notifications as read for the authenticated user.

**Endpoint:** `POST /api/notifications/mark-all-read/`

**Authentication:** Required (Token)

**Request:**
```http
POST /api/notifications/mark-all-read/ HTTP/1.1
Host: localhost:8000
Authorization: Token your_auth_token_here
```

**Success Response (200 OK):**
```json
{
    "message": "5 notification(s) marked as read"
}
```

---

## Usage Examples

### Complete Workflow: Likes and Notifications

#### 1. User Likes a Post

```bash
# Alice likes Bob's post (ID: 5)
curl -X POST http://localhost:8000/api/posts/5/like/ \
  -H "Authorization: Token alice_token_here"

# Response
{
  "message": "You liked the post \"Bob's Amazing Post\"",
  "like": {
    "id": 12,
    "user": "alice",
    "user_id": 1,
    "post": 5,
    "post_id": 5,
    "created_at": "2025-12-14T20:30:00Z"
  }
}
```

**What happens:**
1. Like object created
2. Notification created for Bob (post author)

#### 2. Bob Checks Notifications

```bash
# Bob checks unread notifications
curl -X GET "http://localhost:8000/api/notifications/?unread=true" \
  -H "Authorization: Token bob_token_here"

# Response
[
  {
    "id": 15,
    "recipient": "bob",
    "recipient_id": 2,
    "actor": "alice",
    "actor_id": 1,
    "verb": "liked your post",
    "target_type": "post",
    "target_id": 5,
    "timestamp": "2025-12-14T20:30:00Z",
    "read": false
  }
]
```

#### 3. Bob Marks Notification as Read

```bash
# Bob marks the notification as read
curl -X POST http://localhost:8000/api/notifications/15/read/ \
  -H "Authorization: Token bob_token_here"

# Response
{
  "message": "Notification marked as read",
  "notification": {
    "id": 15,
    "read": true,
    ...
  }
}
```

#### 4. Alice Unlikes the Post

```bash
# Alice changes her mind and unlikes
curl -X POST http://localhost:8000/api/posts/5/unlike/ \
  -H "Authorization: Token alice_token_here"

# Response
{
  "message": "You unliked the post \"Bob's Amazing Post\""
}
```

---

### Python Examples

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
login_response = requests.post(f"{BASE_URL}/login/", json={
    "username": "alice",
    "password": "password123"
})
token = login_response.json()["token"]
headers = {"Authorization": f"Token {token}"}

# Like a post
like_response = requests.post(
    f"{BASE_URL}/posts/5/like/",
    headers=headers
)
print(like_response.json())
# Output: {"message": "You liked the post...", "like": {...}}

# Get all notifications
notifications_response = requests.get(
    f"{BASE_URL}/notifications/",
    headers=headers
)
notifications = notifications_response.json()
print(f"You have {len(notifications)} notifications")

# Get only unread notifications
unread_response = requests.get(
    f"{BASE_URL}/notifications/?unread=true",
    headers=headers
)
unread = unread_response.json()
print(f"You have {len(unread)} unread notifications")

# Mark a notification as read
if unread:
    notification_id = unread[0]['id']
    mark_read_response = requests.post(
        f"{BASE_URL}/notifications/{notification_id}/read/",
        headers=headers
    )
    print(mark_read_response.json())

# Mark all notifications as read
mark_all_response = requests.post(
    f"{BASE_URL}/notifications/mark-all-read/",
    headers=headers
)
print(mark_all_response.json())
# Output: {"message": "5 notification(s) marked as read"}

# Unlike a post
unlike_response = requests.post(
    f"{BASE_URL}/posts/5/unlike/",
    headers=headers
)
print(unlike_response.json())
```

---

### JavaScript Examples

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

// Like a post
async function likePost(postId) {
    const response = await fetch(`${BASE_URL}/posts/${postId}/like/`, {
        method: 'POST',
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Unlike a post
async function unlikePost(postId) {
    const response = await fetch(`${BASE_URL}/posts/${postId}/unlike/`, {
        method: 'POST',
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Get notifications
async function getNotifications(unreadOnly = false) {
    const url = unreadOnly 
        ? `${BASE_URL}/notifications/?unread=true`
        : `${BASE_URL}/notifications/`;
    
    const response = await fetch(url, {
        headers: { 'Authorization': `Token ${authToken}` }
    });
    return await response.json();
}

// Mark notification as read
async function markNotificationRead(notificationId) {
    const response = await fetch(
        `${BASE_URL}/notifications/${notificationId}/read/`,
        {
            method: 'POST',
            headers: { 'Authorization': `Token ${authToken}` }
        }
    );
    return await response.json();
}

// Mark all notifications as read
async function markAllNotificationsRead() {
    const response = await fetch(
        `${BASE_URL}/notifications/mark-all-read/`,
        {
            method: 'POST',
            headers: { 'Authorization': `Token ${authToken}` }
        }
    );
    return await response.json();
}

// Usage
(async () => {
    await login('alice', 'password123');
    
    // Like a post
    const likeResult = await likePost(5);
    console.log(likeResult.message);
    
    // Check unread notifications
    const unread = await getNotifications(true);
    console.log(`${unread.length} unread notifications`);
    
    // Mark all as read
    const markResult = await markAllNotificationsRead();
    console.log(markResult.message);
    
    // Unlike the post
    const unlikeResult = await unlikePost(5);
    console.log(unlikeResult.message);
})();
```

---

## Testing Guide

### Running Tests

```bash
# Run all tests
python manage.py test

# Run only like tests
python manage.py test posts.tests.LikeTestCase

# Run only notification tests
python manage.py test notifications.tests

# Run with verbose output
python manage.py test --verbosity=2
```

### Test Coverage

The implementation includes comprehensive test coverage:

**Like System Tests (9 tests):**
- ✅ Successfully like a post
- ✅ Cannot like post twice
- ✅ Successfully unlike a post
- ✅ Cannot unlike post not liked
- ✅ Like non-existent post returns 404
- ✅ Like requires authentication
- ✅ Like creates notification for post author
- ✅ Liking own post doesn't create notification

**Notification System Tests (11 tests):**
- ✅ Notification model creation
- ✅ Notification string representation
- ✅ Mark notification as read
- ✅ List all notifications
- ✅ List only unread notifications
- ✅ Mark specific notification as read
- ✅ Mark all notifications as read
- ✅ Notifications require authentication
- ✅ Users only see own notifications
- ✅ Cannot mark others' notifications as read

**Total Test Results:**
- **49 tests** total (including previous features)
- **All passing** ✅

### Manual Testing

```bash
# 1. Register/login users
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@test.com","password":"test123","password_confirm":"test123"}'

curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"bob","email":"bob@test.com","password":"test123","password_confirm":"test123"}'

# 2. Bob creates a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token bob_token" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Great content!"}'

# 3. Alice likes Bob's post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token alice_token"

# 4. Bob checks notifications
curl -X GET "http://localhost:8000/api/notifications/?unread=true" \
  -H "Authorization: Token bob_token"

# 5. Bob marks notification as read
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Token bob_token"

# 6. Alice unlikes the post
curl -X POST http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Token alice_token"
```

---

## Notification Trigger Events

Notifications are automatically created for the following events:

### 1. Post Liked
- **Trigger:** User likes a post
- **Recipient:** Post author
- **Verb:** "liked your post"
- **Target:** The post that was liked
- **Exception:** No notification if user likes own post

### 2. Post Commented
- **Trigger:** User comments on a post
- **Recipient:** Post author
- **Verb:** "commented on your post"
- **Target:** The post that was commented on
- **Exception:** No notification if user comments on own post

### 3. User Followed
- **Trigger:** User follows another user
- **Recipient:** User being followed
- **Verb:** "started following you"
- **Target:** The followed user
- **Exception:** Cannot follow yourself (prevented)

---

## Key Features Summary

### Like System
- ✅ Like/unlike posts
- ✅ Unique constraint prevents duplicate likes
- ✅ Creates notifications for post authors
- ✅ Tracks like timestamps
- ✅ Requires authentication
- ✅ Proper error handling

### Notification System
- ✅ Notifications for likes, comments, follows
- ✅ Unread/read status tracking
- ✅ Filter unread notifications
- ✅ Mark individual notification as read
- ✅ Mark all notifications as read
- ✅ Generic ForeignKey for flexible targets
- ✅ Users only see own notifications
- ✅ Ordered by timestamp (newest first)

---

## API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/api/posts/<id>/like/` | ✅ Yes | Like a post |
| POST | `/api/posts/<id>/unlike/` | ✅ Yes | Unlike a post |
| GET | `/api/notifications/` | ✅ Yes | List notifications |
| GET | `/api/notifications/?unread=true` | ✅ Yes | List unread only |
| POST | `/api/notifications/<id>/read/` | ✅ Yes | Mark as read |
| POST | `/api/notifications/mark-all-read/` | ✅ Yes | Mark all as read |

---

## Database Schema

### Like Table
```
┌────────────┬──────────────────┬─────────────────┐
│ Field      │ Type             │ Constraints     │
├────────────┼──────────────────┼─────────────────┤
│ id         │ Integer          │ Primary Key     │
│ user_id    │ ForeignKey       │ Not Null        │
│ post_id    │ ForeignKey       │ Not Null        │
│ created_at │ DateTime         │ Auto            │
└────────────┴──────────────────┴─────────────────┘
Unique: (user_id, post_id)
```

### Notification Table
```
┌─────────────────────┬──────────────────┬─────────────────┐
│ Field               │ Type             │ Constraints     │
├─────────────────────┼──────────────────┼─────────────────┤
│ id                  │ Integer          │ Primary Key     │
│ recipient_id        │ ForeignKey       │ Not Null        │
│ actor_id            │ ForeignKey       │ Not Null        │
│ verb                │ CharField(255)   │ Not Null        │
│ target_content_type │ ForeignKey       │ Nullable        │
│ target_object_id    │ PositiveInt      │ Nullable        │
│ timestamp           │ DateTime         │ Auto            │
│ read                │ Boolean          │ Default: False  │
└─────────────────────┴──────────────────┴─────────────────┘
```

---

## Troubleshooting

### Common Issues

**Issue:** "You have already liked this post"
- **Solution:** Check if like already exists before attempting to like

**Issue:** Notification not created
- **Solution:** Check that user is not performing action on own content

**Issue:** Cannot see notifications
- **Solution:** Ensure you're authenticated and requesting your own notifications

**Issue:** 404 when marking notification as read
- **Solution:** Verify notification ID belongs to authenticated user

---

**Last Updated:** December 14, 2025
**API Version:** 1.0
**Django Version:** 5.2.7
**DRF Version:** 3.15.2
