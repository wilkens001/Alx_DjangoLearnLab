# Project README

This Django project implements a simple library management system with a Book model and basic CRUD operations.

## Project Structure

```
LibraryProject/
├── manage.py
├── LibraryProject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── bookshelf/
    ├── __init__.py
    ├── models.py
    └── migrations/
        └── __init__.py
```

## Setup Instructions

1. Ensure you have Python and Django installed
2. Create and activate a virtual environment
3. Install dependencies
4. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## Features

- Book model with title, author, and publication_year fields
- Complete CRUD operations through Django shell
- Documentation for all CRUD operations