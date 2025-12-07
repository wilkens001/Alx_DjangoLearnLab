# Django Blog Project

A comprehensive Django blog application with user authentication, post management, and a clean user interface.

## Project Structure

```
django_blog/
├── manage.py
├── django_blog/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── blog/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    ├── migrations/
    │   └── __init__.py
    ├── templates/
    │   └── blog/
    │       ├── base.html
    │       └── home.html
    └── static/
        └── blog/
            ├── css/
            │   └── style.css
            └── js/
                └── main.js
```

## Features

- Blog post creation and management
- User authentication with Django's built-in User model
- Clean and responsive design
- Admin interface for managing posts
- Automatic timestamp for published posts

## Installation

1. Ensure Django is installed:
   ```bash
   pip install django
   ```

2. Navigate to the project directory:
   ```bash
   cd django_blog
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application:
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Models

### Post
- **title**: CharField (max 200 characters)
- **content**: TextField
- **published_date**: DateTimeField (auto-generated on creation)
- **author**: ForeignKey to Django's User model

## Usage

1. Log in to the admin panel at `/admin/`
2. Create blog posts through the admin interface
3. View posts on the home page

## Technologies Used

- Django 5.0+
- SQLite (default database)
- HTML/CSS/JavaScript

## Future Enhancements

- Comment system
- Post categories and tags
- User profiles
- Search functionality
- Post editing and deletion from frontend

## License

This project is for educational purposes as part of the ALX Django Learning Lab.
