# Django Library Project

This project demonstrates basic CRUD operations using Django's ORM with a Book model.

## Project Structure

```
LibraryProject/
├── bookshelf/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── LibraryProject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── create.md
├── retrieve.md
├── update.md
├── delete.md
└── manage.py
```

## Model Description

The Book model includes the following fields:
- title: CharField (max_length=200)
- author: CharField (max_length=100)
- publication_year: IntegerField

## CRUD Operations

The project includes detailed documentation for all CRUD operations:
- Create: See create.md
- Retrieve: See retrieve.md
- Update: See update.md
- Delete: See delete.md

Each markdown file contains the exact commands to perform the operations in the Django shell.