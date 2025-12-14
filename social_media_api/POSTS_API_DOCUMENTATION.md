# Posts and Comments API Documentation

## Overview

This documentation covers the Posts and Comments functionality of the Social Media API. Users can create, read, update, and delete posts, as well as comment on posts.

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication

All write operations (POST, PUT, PATCH, DELETE) require authentication using Token Authentication.

**Header Format:**
```
Authorization: Token your_token_here
```

---

## Posts Endpoints

### 1. List All Posts

**Endpoint:** `GET /api/posts/`

**Authentication:** Optional (read-only for unauthenticated users)

**Description:** Retrieve a paginated list of all posts.

**Query Parameters:**
- `page` (integer): Page number for pagination
- `search` (string): Search in title and content
- `ordering` (string): Order by fields (`created_at`, `-created_at`, `updated_at`, `title`)
- `author` (integer): Filter by author ID
- `author__username` (string): Filter by author username

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?page=1&search=django&ordering=-created_at"
```

**Success Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": "johndoe",
      "author_id": 1,
      "title": "Introduction to Django",
      "content": "Django is a high-level Python web framework...",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "comment_count": 5
    }
  ]
}
```

---

### 2. Create a New Post

**Endpoint:** `POST /api/posts/`

**Authentication:** Required

**Description:** Create a new post. The authenticated user becomes the author.

**Request Body:**
```json
{
  "title": "My First Post",
  "content": "This is the content of my first post on this platform!"
}
```

**Success Response (201 Created):**
```json
{
  "id": 10,
  "author": "johndoe",
  "author_id": 1,
  "title": "My First Post",
  "content": "This is the content of my first post on this platform!",
  "created_at": "2024-01-15T14:20:00Z",
  "updated_at": "2024-01-15T14:20:00Z",
  "comment_count": 0,
  "comments": []
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 3. Retrieve a Single Post

**Endpoint:** `GET /api/posts/{post_id}/`

**Authentication:** Optional

**Description:** Retrieve detailed information about a specific post, including all comments.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/posts/1/
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "author": "johndoe",
  "author_id": 1,
  "title": "Introduction to Django",
  "content": "Django is a high-level Python web framework...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "comment_count": 2,
  "comments": [
    {
      "id": 1,
      "post": 1,
      "post_id": 1,
      "author": "janedoe",
      "author_id": 2,
      "content": "Great post!",
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 4. Update a Post

**Endpoint:** `PUT /api/posts/{post_id}/` or `PATCH /api/posts/{post_id}/`

**Authentication:** Required (must be the post author)

**Description:** Update an existing post. Only the author can update their posts.

**Request Body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content here..."
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "author": "johndoe",
  "author_id": 1,
  "title": "Updated Title",
  "content": "Updated content here...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T14:45:00Z",
  "comment_count": 2,
  "comments": [...]
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 5. Delete a Post

**Endpoint:** `DELETE /api/posts/{post_id}/`

**Authentication:** Required (must be the post author)

**Description:** Delete a post. Only the author can delete their posts. This also deletes all associated comments.

**Success Response (204 No Content)**

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 6. Get Post Comments

**Endpoint:** `GET /api/posts/{post_id}/comments/`

**Authentication:** Optional

**Description:** Retrieve all comments for a specific post (custom action).

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "post": 1,
    "post_id": 1,
    "author": "janedoe",
    "author_id": 2,
    "content": "Great post!",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
]
```

---

## Comments Endpoints

### 1. List All Comments

**Endpoint:** `GET /api/comments/`

**Authentication:** Optional

**Description:** Retrieve a paginated list of all comments.

**Query Parameters:**
- `page` (integer): Page number for pagination
- `post` (integer): Filter by post ID
- `author` (integer): Filter by author ID
- `author__username` (string): Filter by author username
- `ordering` (string): Order by fields (`created_at`, `-created_at`, `updated_at`)

**Example Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/comments/?post=1"
```

**Success Response (200 OK):**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "post": 1,
      "post_id": 1,
      "author": "janedoe",
      "author_id": 2,
      "content": "Great post!",
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z"
    }
  ]
}
```

---

### 2. Create a Comment

**Endpoint:** `POST /api/comments/`

**Authentication:** Required

**Description:** Create a new comment on a post.

**Request Body:**
```json
{
  "post": 1,
  "content": "This is an insightful comment!"
}
```

**Success Response (201 Created):**
```json
{
  "id": 15,
  "post": 1,
  "post_id": 1,
  "author": "johndoe",
  "author_id": 1,
  "content": "This is an insightful comment!",
  "created_at": "2024-01-15T15:00:00Z",
  "updated_at": "2024-01-15T15:00:00Z"
}
```

---

### 3. Retrieve a Single Comment

**Endpoint:** `GET /api/comments/{comment_id}/`

**Authentication:** Optional

**Description:** Retrieve detailed information about a specific comment.

**Success Response (200 OK):**
```json
{
  "id": 1,
  "post": 1,
  "post_id": 1,
  "author": "janedoe",
  "author_id": 2,
  "content": "Great post!",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

---

### 4. Update a Comment

**Endpoint:** `PUT /api/comments/{comment_id}/` or `PATCH /api/comments/{comment_id}/`

**Authentication:** Required (must be the comment author)

**Description:** Update an existing comment. Only the author can update their comments.

**Request Body:**
```json
{
  "post": 1,
  "content": "Updated comment content"
}
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "post": 1,
  "post_id": 1,
  "author": "janedoe",
  "author_id": 2,
  "content": "Updated comment content",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T15:30:00Z"
}
```

---

### 5. Delete a Comment

**Endpoint:** `DELETE /api/comments/{comment_id}/`

**Authentication:** Required (must be the comment author)

**Description:** Delete a comment. Only the author can delete their comments.

**Success Response (204 No Content)**

---

## Filtering and Search Examples

### Search Posts by Title or Content
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?search=django"
```

### Filter Posts by Author Username
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?author__username=johndoe"
```

### Order Posts by Most Recent
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?ordering=-created_at"
```

### Get Comments for Specific Post
```bash
curl -X GET "http://127.0.0.1:8000/api/comments/?post=1"
```

### Combine Multiple Filters
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?search=django&author__username=johndoe&ordering=-created_at"
```

---

## Pagination

All list endpoints support pagination with the following response format:

```json
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/posts/?page=3",
  "previous": "http://127.0.0.1:8000/api/posts/?page=1",
  "results": [...]
}
```

**Default page size:** 10 items per page

**Access specific page:**
```bash
curl -X GET "http://127.0.0.1:8000/api/posts/?page=2"
```

---

## Permissions

### Post Permissions
- **List/Retrieve**: Anyone (no authentication required)
- **Create**: Authenticated users only
- **Update/Delete**: Only the post author

### Comment Permissions
- **List/Retrieve**: Anyone (no authentication required)
- **Create**: Authenticated users only
- **Update/Delete**: Only the comment author

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message describing the validation error."]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Complete Usage Examples

### Example: Create a Post and Add Comments

**1. Authenticate and get token:**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password123"}'
```

**2. Create a post:**
```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Awesome Post",
    "content": "This is the content of my post."
  }'
```

**3. Add a comment:**
```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

**4. Update the post:**
```bash
curl -X PATCH http://127.0.0.1:8000/api/posts/1/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Updated Awesome Post"
  }'
```

**5. Delete the comment:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/comments/1/ \
  -H "Authorization: Token your_token_here"
```

---

## Python Requests Examples

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"
token = "your_token_here"
headers = {"Authorization": f"Token {token}"}

# Create a post
post_data = {
    "title": "Python API Example",
    "content": "This post was created using Python requests!"
}
response = requests.post(f"{BASE_URL}/posts/", json=post_data, headers=headers)
post_id = response.json()['id']

# Get all posts
response = requests.get(f"{BASE_URL}/posts/")
posts = response.json()['results']

# Add a comment
comment_data = {
    "post": post_id,
    "content": "Automated comment via API"
}
response = requests.post(f"{BASE_URL}/comments/", json=comment_data, headers=headers)

# Search posts
response = requests.get(f"{BASE_URL}/posts/", params={"search": "Python"})
```

---

## Testing with Postman

### Collection Structure

1. **Posts**
   - List Posts (GET)
   - Create Post (POST)
   - Get Post Detail (GET)
   - Update Post (PUT/PATCH)
   - Delete Post (DELETE)
   - Get Post Comments (GET)

2. **Comments**
   - List Comments (GET)
   - Create Comment (POST)
   - Get Comment Detail (GET)
   - Update Comment (PUT/PATCH)
   - Delete Comment (DELETE)

### Environment Variables
- `base_url`: `http://127.0.0.1:8000/api`
- `token`: Your authentication token
- `post_id`: ID of a test post
- `comment_id`: ID of a test comment

---

## Summary

The Posts and Comments API provides full CRUD functionality with:
- ✅ Token-based authentication
- ✅ Author-based permissions
- ✅ Pagination (10 items per page)
- ✅ Filtering by author and post
- ✅ Full-text search in posts
- ✅ Ordering options
- ✅ Nested comment data in posts
- ✅ RESTful design principles

For more information, see the main API documentation.
