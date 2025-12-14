# Social Media API

A Django REST Framework-based social media API with user authentication, profile management, and social features.

## Project Overview

This Social Media API provides a robust backend for a social media platform, featuring:
- User registration and authentication
- Token-based authentication
- Custom user profiles with bio and profile pictures
- Follow/unfollow functionality
- Posts and comments management
- RESTful API endpoints

## Features

### User Authentication
- **User Registration**: Create new user accounts with email verification
- **User Login**: Authenticate users and receive authentication tokens
- **Token Authentication**: Secure API endpoints using token-based authentication

### User Profile Management
- **Custom User Model**: Extended user model with additional fields:
  - `bio`: User biography (max 500 characters)
  - `profile_picture`: User profile image
  - `followers`: Many-to-many relationship for following other users
- **Profile Endpoints**: View and update user profiles
- **User Discovery**: List and search for other users

### Posts and Comments
- **Create Posts**: Authenticated users can create posts
- **CRUD Operations**: Full create, read, update, delete for posts and comments
- **Author Permissions**: Only authors can edit/delete their own content
- **Pagination**: Efficient handling of large datasets
- **Filtering & Search**: Search posts by title/content, filter by author
- **Nested Comments**: View all comments within post details

## Technology Stack

- **Django 5.2**: Web framework
- **Django REST Framework**: API development
- **django-filter**: Advanced filtering capabilities
- **Token Authentication**: Secure API access
- **SQLite**: Database (development)
- **Pillow**: Image processing for profile pictures

## Project Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/social_media_api
   ```

2. **Create and activate a virtual environment:**
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages:**
   ```bash
   pip install django djangorestframework pillow
   ```

4. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### Register a New User
- **URL**: `/api/register/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
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
- **Success Response** (201 Created):
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

#### Login
- **URL**: `/api/login/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Success Response** (200 OK):
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

### Profile Endpoints

#### Get Current User Profile
- **URL**: `/api/profile/`
- **Method**: `GET`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **Success Response** (200 OK):
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
    "followers": [2, 3, 5],
    "following": [4, 6, 7]
  }
  ```

#### Update User Profile
- **URL**: `/api/profile/`
- **Method**: `PUT` or `PATCH`
- **Authentication**: Required (Token)
- **Headers**:
  ```
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```
- **Request Body**:
  ```json
  {
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Updated bio text"
  }
  ```
- **Success Response** (200 OK): Returns updated profile data

#### List All Users
- **URL**: `/api/users/`
- **Method**: `GET`
- **Authentication**: Optional
- **Success Response** (200 OK): Returns array of user profiles

#### Get Specific User Profile
- **URL**: `/api/users/<user_id>/`
- **Method**: `GET`
- **Authentication**: Optional
- **Success Response** (200 OK): Returns user profile data

## Authentication

This API uses Token Authentication. To access protected endpoints:

1. **Obtain a token** by registering or logging in
2. **Include the token** in the Authorization header for subsequent requests:
   ```
   Authorization: Token your_token_here
   ```

### Example with curl:
```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password_confirm":"testpass123"}'

# Login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get profile (with token)
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Token your_token_here"
```

## User Model Structure

The custom user model extends Django's `AbstractUser` and includes:

| Field | Type | Description |
|-------|------|-------------|
| username | String | Unique username (inherited) |
| email | Email | User email address (inherited) |
| password | String | Hashed password (inherited) |
| first_name | String | First name (inherited) |
| last_name | String | Last name (inherited) |
| bio | TextField | User biography (max 500 chars) |
| profile_picture | ImageField | Profile picture upload |
| followers | ManyToMany | Users who follow this user |
| date_joined | DateTime | Registration date (inherited) |

### Relationships

- **Followers**: Self-referential many-to-many relationship
  - `user.followers.all()` - Get all followers
  - `user.following.all()` - Get all users being followed
  - `symmetrical=False` - Following is not bidirectional

## Testing with Postman

### 1. Register a New User

1. Open Postman
2. Create a new `POST` request to `http://127.0.0.1:8000/api/register/`
3. Go to the "Body" tab, select "raw" and "JSON"
4. Enter the registration data:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "password_confirm": "testpass123",
     "bio": "This is my bio"
   }
   ```
5. Click "Send"
6. Copy the token from the response

### 2. Login

1. Create a new `POST` request to `http://127.0.0.1:8000/api/login/`
2. Body (JSON):
   ```json
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```
3. Copy the token from the response

### 3. Get Profile (Authenticated Request)

1. Create a new `GET` request to `http://127.0.0.1:8000/api/profile/`
2. Go to the "Headers" tab
3. Add header:
   - Key: `Authorization`
   - Value: `Token your_token_here`
4. Click "Send"

### 4. Update Profile

1. Create a new `PATCH` request to `http://127.0.0.1:8000/api/profile/`
2. Add the Authorization header (same as above)
3. Body (JSON):
   ```json
   {
     "bio": "Updated bio text",
     "first_name": "John"
   }
   ```
4. Click "Send"

## Running Tests

Run the automated tests:

```bash
python manage.py test accounts
```

## Project Structure

```
social_media_api/
├── manage.py
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── accounts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py          # Custom User model
    ├── serializers.py     # DRF serializers
    ├── views.py           # API views
    ├── urls.py            # URL routing
    ├── tests.py           # Test cases
    └── migrations/
        └── __init__.py
```

## Development Notes

### Custom User Model

The custom user model must be set before running initial migrations:
```python
# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Media Files

Profile pictures are stored in `media/profile_pictures/`. Ensure the media directory is configured:
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Security Considerations

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use environment variables for sensitive data
- Implement HTTPS in production
- Add rate limiting for authentication endpoints

## Future Enhancements

- Password reset functionality
- Email verification
- Social authentication (OAuth)
- Posts and comments
- Likes and reactions
- Direct messaging
- Notifications
- Search functionality
- Feed algorithm

## Troubleshooting

### Issue: "No module named 'PIL'"
**Solution**: Install Pillow: `pip install pillow`

### Issue: Migration errors
**Solution**: Delete `db.sqlite3` and all migration files (except `__init__.py`), then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Token not working
**Solution**: Ensure the Authorization header is properly formatted:
```
Authorization: Token your_token_here
```
(Note: "Token" not "Bearer")

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the ALX Django Learning Lab.

## Contact

For questions or support, please contact the development team.

---

**Note**: This is a development version. Additional security measures should be implemented before deploying to production.
