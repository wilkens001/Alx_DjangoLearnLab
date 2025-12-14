# Social Media API

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-ALX-orange.svg)](https://www.alxafrica.com/)

A comprehensive Django REST Framework-based social media API with user authentication, social features, posts, comments, likes, follows, and real-time notifications.

## 📋 Project Overview

This Social Media API provides a complete backend for a modern social media platform featuring:
- 🔐 User registration and token-based authentication
- 👤 Custom user profiles with bio and profile pictures
- 📝 Posts and comments with full CRUD operations
- ❤️ Like/unlike functionality
- 👥 Follow/unfollow system
- 📰 Personalized feed showing posts from followed users
- 🔔 Real-time notifications for likes, comments, and follows
- 🔍 Search and filtering capabilities
- 📄 Pagination for all list endpoints
- 🚀 Production-ready with deployment configuration

## ✨ Features

### User Authentication & Profiles
- ✅ User registration with email validation
- ✅ Token-based authentication
- ✅ Login/logout functionality
- ✅ Custom user profiles (bio, profile picture)
- ✅ Profile viewing and updates
- ✅ User discovery and search

### Social Features
- ✅ Follow/unfollow users
- ✅ Follower/following counts
- ✅ Personalized feed (posts from followed users)
- ✅ Activity tracking

### Posts & Comments
- ✅ Create, read, update, delete posts
- ✅ Comment on posts
- ✅ Author-only permissions for editing
- ✅ Pagination (10 items per page)
- ✅ Search posts by title/content
- ✅ Filter by author

### Engagement Features
- ✅ Like/unlike posts
- ✅ Like count tracking
- ✅ Duplicate like prevention
- ✅ Author notifications on likes

### Notifications System
- ✅ Notifications for:
  - New followers
  - Post likes
  - Post comments
- ✅ Read/unread status tracking
- ✅ Mark individual notification as read
- ✅ Mark all notifications as read
- ✅ Filter notifications by read status

### Production Ready
- ✅ Environment variable configuration
- ✅ Security headers enabled
- ✅ PostgreSQL support
- ✅ Static files handling (WhiteNoise)
- ✅ AWS S3 support for media files
- ✅ Gunicorn WSGI server configuration
- ✅ Nginx reverse proxy setup
- ✅ Comprehensive deployment documentation

## 🛠️ Technology Stack

- **Django 5.2**: Web framework
- **Django REST Framework 3.14+**: API development
- **django-filter 23.0+**: Advanced filtering capabilities
- **Token Authentication**: Secure API access
- **PostgreSQL**: Production database
- **SQLite**: Development database
- **Pillow 10.0+**: Image processing for profile pictures
- **Gunicorn**: Production WSGI server
- **WhiteNoise**: Static file serving
- **python-decouple**: Environment variable management
- **dj-database-url**: Database configuration
- **django-storages & boto3**: AWS S3 integration (optional)

## 📦 Project Setup

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- PostgreSQL (for production)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/wilkens001/Alx_DjangoLearnLab.git
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
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## 🌐 API Endpoints

### Base URL
- Development: `http://127.0.0.1:8000/api/`
- Production: `https://your-domain.com/api/`

### Authentication Endpoints

#### Register a New User
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "bio": "Software developer and tech enthusiast"
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
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
  ```

#### Login
- **URL**: `/api/accounts/login/`
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
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com"
    }
  }
  ```

#### Logout
- **URL**: `/api/accounts/logout/`
- **Method**: `POST`
- **Authentication**: Required (Token)

### Profile Endpoints

#### Get Current User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `GET`
- **Authentication**: Required (Token)

#### Update User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `PUT` or `PATCH`
- **Authentication**: Required (Token)

### Posts & Comments Endpoints

#### List All Posts
- **URL**: `/api/posts/`
- **Method**: `GET`
- **Query Parameters**:
  - `search`: Search by title or content
  - `author__username`: Filter by author
  - `page`: Page number

#### Create Post
- **URL**: `/api/posts/`
- **Method**: `POST`
- **Authentication**: Required (Token)
- **Request Body**:
  ```json
  {
    "title": "My First Post",
    "content": "This is the content of my post..."
  }
  ```

#### Get/Update/Delete Post
- **URL**: `/api/posts/<id>/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required for update/delete (must be author)

#### List Comments
- **URL**: `/api/comments/`
- **Method**: `GET`
- **Query Parameters**:
  - `post`: Filter by post ID

#### Create Comment
- **URL**: `/api/comments/`
- **Method**: `POST`
- **Authentication**: Required (Token)
- **Request Body**:
  ```json
  {
    "post": 1,
    "content": "Great post!"
  }
  ```

### Like Endpoints

#### Like a Post
- **URL**: `/api/posts/<id>/like/`
- **Method**: `POST`
- **Authentication**: Required (Token)

#### Unlike a Post
- **URL**: `/api/posts/<id>/unlike/`
- **Method**: `POST`
- **Authentication**: Required (Token)

### Follow Management Endpoints

#### Follow a User
- **URL**: `/api/accounts/follow/<user_id>/`
- **Method**: `POST`
- **Authentication**: Required (Token)

#### Unfollow a User
- **URL**: `/api/accounts/unfollow/<user_id>/`
- **Method**: `POST`
- **Authentication**: Required (Token)

### Feed Endpoint

#### Get Personalized Feed
- **URL**: `/api/feed/`
- **Method**: `GET`
- **Authentication**: Required (Token)
- **Description**: Returns posts from users you follow, ordered by creation date

### Notifications Endpoints

#### List Notifications
- **URL**: `/api/notifications/`
- **Method**: `GET`
- **Authentication**: Required (Token)
- **Query Parameters**:
  - `read`: Filter by read status (`true`/`false`)

#### Mark Notification as Read
- **URL**: `/api/notifications/<id>/read/`
- **Method**: `POST`
- **Authentication**: Required (Token)

#### Mark All Notifications as Read
- **URL**: `/api/notifications/mark-all-read/`
- **Method**: `POST`
- **Authentication**: Required (Token)

## 🔐 Authentication

This API uses Token Authentication. To access protected endpoints:

1. **Obtain a token** by registering or logging in
2. **Include the token** in the Authorization header for subsequent requests:
   ```
   Authorization: Token your_token_here
   ```

### Example with curl:
```bash
# Register a new user
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123","bio":"Test user"}'

# Login
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Get profile (with token)
curl -X GET http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token your_token_here"

# Create a post
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"This is my post content"}'
```

## 🧪 Running Tests

The project includes a comprehensive test suite with **49 tests** covering all features:

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test posts
python manage.py test notifications

# Run with coverage
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

**Test Coverage:**
- Authentication: 13 tests ✅
- Posts & Comments: 13 tests ✅
- Follows & Feed: 17 tests ✅
- Likes: 9 tests ✅
- Notifications: 11 tests ✅

**Total: 49 tests** - All passing ✅

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

## 📁 Project Structure

```
social_media_api/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── Procfile                       # Heroku configuration
├── runtime.txt                    # Python version for deployment
├── gunicorn_config.py            # Gunicorn configuration
├── nginx.conf                    # Nginx configuration
├── db.sqlite3                    # Development database
├── logs/                         # Application logs
├── staticfiles/                  # Collected static files
├── media/                        # User uploaded files
├── social_media_api/             # Project settings
│   ├── settings.py               # Development settings
│   ├── settings_production.py   # Production settings
│   ├── urls.py                   # URL routing
│   └── wsgi.py                   # WSGI application
├── accounts/                     # User authentication app
│   ├── models.py                 # CustomUser model
│   ├── serializers.py            # User serializers
│   ├── views.py                  # Auth views
│   ├── urls.py                   # Auth URLs
│   └── tests.py                  # Auth tests (13 tests)
├── posts/                        # Posts, comments, likes app
│   ├── models.py                 # Post, Comment, Like models
│   ├── serializers.py            # Post serializers
│   ├── views.py                  # Post views
│   ├── urls.py                   # Post URLs
│   ├── permissions.py            # Custom permissions
│   └── tests.py                  # Post tests (22 tests)
├── notifications/                # Notifications app
│   ├── models.py                 # Notification model
│   ├── serializers.py            # Notification serializers
│   ├── views.py                  # Notification views
│   ├── urls.py                   # Notification URLs
│   └── tests.py                  # Notification tests (11 tests)
└── Documentation/                # Project documentation
    ├── README.md                 # This file
    ├── DEPLOYMENT.md             # Full deployment guide
    ├── QUICK_DEPLOY.md           # Quick deployment guide
    ├── DEPLOY_WITHOUT_CLI.md     # Deploy without Heroku CLI
    ├── README_DEPLOYMENT.md      # Deployment overview
    └── TASK_*_COMPLETION.md      # Task completion docs
```

## 🚀 Deployment

The project is production-ready and can be deployed to various platforms:

### Deployment Options

1. **Heroku** (Easiest - Web Dashboard)
   - See: `DEPLOY_WITHOUT_CLI.md`
   - Free tier available
   - Automatic SSL

2. **Render.com** (Heroku Alternative)
   - Free tier available
   - GitHub integration

3. **Railway.app** (Modern Platform)
   - Automatic deploys
   - Free tier

4. **DigitalOcean** App Platform
   - Managed hosting
   - $5/month minimum

5. **VPS** (Full Control)
   - Ubuntu/Debian server
   - Manual setup required

### Quick Deploy to Heroku

See `QUICK_DEPLOY.md` for step-by-step instructions.

### Environment Variables

Required for production:
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://user:pass@host:port/db
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Deployment Documentation

- **Full Guide**: `DEPLOYMENT.md` (700+ lines)
- **Quick Start**: `QUICK_DEPLOY.md`
- **No CLI**: `DEPLOY_WITHOUT_CLI.md`
- **Overview**: `README_DEPLOYMENT.md`

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of the ALX Django Learning Lab curriculum.

## 👥 Authors

- **wilkens001** - [GitHub](https://github.com/wilkens001)

## 🔗 Links

- **Repository**: https://github.com/wilkens001/Alx_DjangoLearnLab
- **Directory**: `social_media_api`
- **Documentation**: See `DEPLOYMENT.md` and other docs

## ✨ Acknowledgments

- ALX Africa for the curriculum
- Django and DRF communities
- All contributors and reviewers

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation files
- Review the troubleshooting section above

---

**Project Status**: ✅ Production Ready  
**Last Updated**: December 14, 2025  
**Version**: 1.0.0  

**Repository**: https://github.com/wilkens001/Alx_DjangoLearnLab  
**Public Access**: ✅ Enabled for Review
