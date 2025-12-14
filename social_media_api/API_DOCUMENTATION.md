# API Documentation - Social Media API

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
Most endpoints require authentication using Token Authentication.

**Header Format:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

---

## Endpoints

### 1. User Registration

**Endpoint:** `POST /api/register/`

**Authentication:** Not required

**Description:** Register a new user account and receive an authentication token.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "bio": "Software developer and tech enthusiast",
  "profile_picture": null
}
```

**Required Fields:**
- `username` (string): Unique username
- `email` (string): Valid email address
- `password` (string): User password (min 8 characters recommended)
- `password_confirm` (string): Must match password

**Optional Fields:**
- `bio` (string): User biography (max 500 characters)
- `profile_picture` (file): Profile image upload

**Success Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer and tech enthusiast"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "password": ["Passwords do not match."]
}
```

---

### 2. User Login

**Endpoint:** `POST /api/login/`

**Authentication:** Not required

**Description:** Authenticate user credentials and receive an authentication token.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Success Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer and tech enthusiast"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid username or password"
}
```

---

### 3. Get Current User Profile

**Endpoint:** `GET /api/profile/`

**Authentication:** Required (Token)

**Description:** Retrieve the authenticated user's profile information.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer and tech enthusiast",
  "profile_picture": "/media/profile_pictures/john.jpg",
  "date_joined": "2024-01-15T10:30:00Z",
  "followers_count": 150,
  "following_count": 200,
  "followers": [2, 3, 5, 8],
  "following": [4, 6, 7, 9]
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 4. Update User Profile

**Endpoint:** `PUT /api/profile/` or `PATCH /api/profile/`

**Authentication:** Required (Token)

**Description:** Update the authenticated user's profile information.

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body (all fields optional):**
```json
{
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated biography text"
}
```

**Editable Fields:**
- `email` (string): Email address
- `first_name` (string): First name
- `last_name` (string): Last name
- `bio` (string): Biography (max 500 characters)
- `profile_picture` (file): Profile picture

**Success Response (200 OK):**
```json
{
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated biography text",
  "profile_picture": "/media/profile_pictures/john.jpg"
}
```

---

### 5. List All Users

**Endpoint:** `GET /api/users/`

**Authentication:** Optional (readable by anyone, authentication recommended)

**Description:** Retrieve a list of all registered users.

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer",
    "profile_picture": "/media/profile_pictures/john.jpg",
    "date_joined": "2024-01-15T10:30:00Z",
    "followers_count": 150,
    "following_count": 200,
    "followers": [2, 3],
    "following": [4, 5]
  },
  {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "bio": "Designer and artist",
    "profile_picture": "/media/profile_pictures/jane.jpg",
    "date_joined": "2024-01-16T11:00:00Z",
    "followers_count": 200,
    "following_count": 180,
    "followers": [1, 3],
    "following": [1, 4]
  }
]
```

---

### 6. Get User Detail

**Endpoint:** `GET /api/users/<user_id>/`

**Authentication:** Optional

**Description:** Retrieve detailed information about a specific user.

**Example:** `GET /api/users/1/`

**Success Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer and tech enthusiast",
  "profile_picture": "/media/profile_pictures/john.jpg",
  "date_joined": "2024-01-15T10:30:00Z",
  "followers_count": 150,
  "following_count": 200,
  "followers": [2, 3, 5, 8],
  "following": [4, 6, 7, 9]
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

## Response Fields Explained

### User Profile Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique user identifier |
| `username` | String | Unique username |
| `email` | String | User's email address |
| `first_name` | String | User's first name (optional) |
| `last_name` | String | User's last name (optional) |
| `bio` | String | User biography (max 500 chars) |
| `profile_picture` | String/URL | URL to profile picture |
| `date_joined` | DateTime | Registration timestamp (ISO 8601) |
| `followers_count` | Integer | Number of followers |
| `following_count` | Integer | Number of users being followed |
| `followers` | Array | List of follower user IDs |
| `following` | Array | List of followed user IDs |

---

## Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid data or validation error |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server-side error |

---

## Testing with cURL

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Test bio"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### Get Profile
```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Update Profile
```bash
curl -X PATCH http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "bio": "Updated bio",
    "first_name": "Test"
  }'
```

### List Users
```bash
curl -X GET http://127.0.0.1:8000/api/users/
```

---

## Testing with Python Requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Register
response = requests.post(f"{BASE_URL}/register/", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
})
token = response.json()['token']

# Get profile
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/profile/", headers=headers)
print(response.json())
```

---

## Rate Limiting

Currently, no rate limiting is implemented. In production:
- Implement rate limiting for authentication endpoints
- Use `django-ratelimit` or similar packages
- Recommended: 5 login attempts per minute

---

## Security Notes

1. **HTTPS Required in Production**: Always use HTTPS in production
2. **Token Security**: Store tokens securely, never in version control
3. **Password Requirements**: Enforce strong passwords (min 8 chars, mixed case, numbers)
4. **CORS Configuration**: Configure CORS for frontend applications
5. **Environment Variables**: Use environment variables for sensitive settings

---

## Support

For more information, see the main README.md file.
