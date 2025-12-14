# Social Media API - Quick Start Guide

## Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- Django (>=5.0)
- Django REST Framework (>=3.14.0)
- Pillow (>=10.0.0)

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Start Development Server
```bash
python manage.py runserver
```

Server will be available at: `http://127.0.0.1:8000/`

## Quick API Test

### Register a User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "bio": "Test user"
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

**Save the token from the response!**

### Get Profile (with token)
```bash
curl -X GET http://127.0.0.1:8000/api/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/api/register/` | POST | No | Register new user |
| `/api/login/` | POST | No | Login user |
| `/api/profile/` | GET | Yes | Get current user profile |
| `/api/profile/` | PUT/PATCH | Yes | Update profile |
| `/api/users/` | GET | Optional | List all users |
| `/api/users/<id>/` | GET | Optional | Get user detail |

## Admin Interface

Access the Django admin at: `http://127.0.0.1:8000/admin/`

Login with the superuser credentials you created.

## Running Tests

```bash
python manage.py test accounts
```

## Project Structure

```
social_media_api/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # Full documentation
├── SETUP.md                     # This file
├── db.sqlite3                   # Database (created after migrations)
├── social_media_api/            # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
└── accounts/                    # Accounts app
    ├── models.py               # CustomUser model
    ├── serializers.py          # API serializers
    ├── views.py                # API views
    ├── urls.py                 # App URL patterns
    ├── admin.py                # Admin configuration
    ├── tests.py                # Test cases
    └── migrations/             # Database migrations
        └── 0001_initial.py
```

## Troubleshooting

**Issue**: "No module named 'PIL'"
```bash
pip install Pillow
```

**Issue**: "Table already exists"
```bash
# Delete db.sqlite3 and run migrations again
python manage.py migrate
```

**Issue**: Token authentication not working
- Make sure header is: `Authorization: Token YOUR_TOKEN`
- Not "Bearer", use "Token"

## Next Steps

1. Read the full README.md for detailed documentation
2. Test all endpoints using Postman or curl
3. Explore the Django admin interface
4. Run the test suite
5. Start building additional features!

## Support

For detailed information, see the main README.md file.
