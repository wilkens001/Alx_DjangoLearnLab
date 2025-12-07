# Advanced API Project

This Django project demonstrates advanced API development with Django REST Framework, focusing on custom serializers that handle complex data structures and nested relationships.

## Project Overview

This project implements a simple book management API with two models:
- **Author**: Represents book authors
- **Book**: Represents books with a foreign key relationship to authors

The project showcases:
- Custom serializers with nested relationships
- Data validation in serializers
- One-to-many relationships between models
- Django REST Framework integration

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd advanced-api-project
   ```

2. **Install required packages:**
   ```bash
   pip install django djangorestframework
   ```

3. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
advanced-api-project/
├── advanced_api_project/      # Project settings
│   ├── settings.py            # Django settings with REST framework configured
│   ├── urls.py                # Main URL configuration
│   └── ...
├── api/                       # Main API application
│   ├── models.py              # Author and Book models
│   ├── serializers.py         # Custom serializers
│   ├── admin.py               # Admin configuration
│   ├── migrations/            # Database migrations
│   └── ...
├── manage.py                  # Django management script
├── test_serializers.py        # Test script for models and serializers
└── README.md                  # This file
```

## Models

### Author Model
Represents a book author with the following field:
- `name` (CharField): The author's full name (max 100 characters)

**Relationship**: One-to-many with Book (one author can have multiple books)

### Book Model
Represents a book with the following fields:
- `title` (CharField): The book's title (max 200 characters)
- `publication_year` (IntegerField): The year the book was published
- `author` (ForeignKey): Reference to the Author model

**Relationship**: Many-to-one with Author (each book belongs to one author)

## Serializers

### BookSerializer
A ModelSerializer that handles all fields of the Book model.

**Features:**
- Serializes all Book fields (id, title, publication_year, author)
- Custom validation to ensure publication_year is not in the future
- Provides detailed error messages for validation failures

**Custom Validation:**
```python
def validate_publication_year(self, value):
    """Ensures the publication year is not in the future."""
    current_year = datetime.now().year
    if value > current_year:
        raise serializers.ValidationError(
            f"Publication year cannot be in the future. Current year is {current_year}."
        )
    return value
```

### AuthorSerializer
A ModelSerializer that includes nested Book serialization.

**Features:**
- Serializes Author fields (id, name)
- Includes a nested representation of all books by the author
- Demonstrates handling of one-to-many relationships
- Uses BookSerializer for nested book data

**Nested Relationship Handling:**
The serializer uses the `related_name='books'` from the Book model's foreign key to access all books for an author:

```python
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
```

**Example JSON Output:**
```json
{
    "id": 1,
    "name": "J.K. Rowling",
    "books": [
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        },
        {
            "id": 2,
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": 1
        }
    ]
}
```

## Testing

### Using the Test Script

Run the included test script to verify the functionality:

```bash
python test_serializers.py
```

This script tests:
1. Creating Author and Book instances
2. Serializing individual books
3. Serializing authors with nested books
4. Validation of publication years (valid and invalid cases)
5. Reverse relationship queries (author.books.all())
6. Serializing multiple authors

### Using Django Shell

You can also test interactively using the Django shell:

```bash
python manage.py shell
```

```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

# Create an author
author = Author.objects.create(name="J.K. Rowling")

# Create books
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author
)

# Serialize the author with nested books
serializer = AuthorSerializer(author)
print(serializer.data)

# Test validation
serializer = BookSerializer(data={
    'title': 'Test Book',
    'publication_year': 2030,  # Future year
    'author': author.id
})
print(serializer.is_valid())  # Should be False
print(serializer.errors)
```

### Using Django Admin

1. Start the server: `python manage.py runserver`
2. Navigate to: `http://127.0.0.1:8000/admin/`
3. Log in with your superuser credentials
4. Create and manage Authors and Books through the admin interface

## Key Features Demonstrated

### 1. Custom Serializers
- **BookSerializer**: Basic ModelSerializer with custom validation
- **AuthorSerializer**: Advanced serializer with nested relationships

### 2. Data Validation
- Custom `validate_publication_year` method ensures data integrity
- Prevents future publication years with descriptive error messages

### 3. Nested Serialization
- AuthorSerializer includes nested BookSerializer
- Demonstrates one-to-many relationship handling
- Uses `many=True` for multiple related objects
- Uses `read_only=True` for output-only nested data

### 4. Relationship Handling
- Foreign key relationship from Book to Author
- Reverse relationship using `related_name='books'`
- Cascade deletion (when an author is deleted, their books are also deleted)

## Configuration Details

### Settings (advanced_api_project/settings.py)

The project has been configured with:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'api',             # Our API application
]
```

### Database
- Uses SQLite by default (db.sqlite3)
- Can be configured to use other databases in settings.py

## Learning Outcomes

By completing this project, you will understand:

1. How to set up a Django project with Django REST Framework
2. How to create models with foreign key relationships
3. How to create custom serializers with validation
4. How to implement nested serialization for related objects
5. How to handle one-to-many relationships in serializers
6. How to validate data in serializers
7. How to test models and serializers

## Next Steps

To extend this project, consider:

1. Creating API views to expose the serializers
2. Adding URL patterns for API endpoints
3. Implementing filtering and pagination
4. Adding authentication and permissions
5. Creating additional models and relationships
6. Implementing more complex validation logic
7. Adding unit tests using Django's TestCase

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django REST Framework Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django REST Framework Relations](https://www.django-rest-framework.org/api-guide/relations/)
