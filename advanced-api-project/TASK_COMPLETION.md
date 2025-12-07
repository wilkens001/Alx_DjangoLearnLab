# Task 0: Setting Up a New Django Project with Custom Serializers

## ✅ Task Completion Summary

All requirements for Task 0 have been successfully completed. Below is a detailed breakdown of what was implemented.

---

## Step 1: Install Django and Django REST Framework ✅

**Completed Actions:**
- ✅ Installed Django (version 5.2.7)
- ✅ Installed Django REST Framework (latest version)
- ✅ Created Django project named `advanced_api_project` in the `advanced-api-project` directory
- ✅ Created Django app named `api` inside the project

**Command Used:**
```bash
pip install django djangorestframework
django-admin startproject advanced_api_project .
python manage.py startapp api
```

---

## Step 2: Configure the Project ✅

**Completed Actions:**
- ✅ Added `rest_framework` to `INSTALLED_APPS` in `settings.py`
- ✅ Added `api` app to `INSTALLED_APPS`
- ✅ Configured to use Django's default SQLite database

**Configuration in settings.py:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Added
    'api',             # Added
]
```

---

## Step 3: Define Data Models ✅

**Completed Actions:**
- ✅ Created `Author` model with `name` field (CharField, max_length=100)
- ✅ Created `Book` model with:
  - `title` field (CharField, max_length=200)
  - `publication_year` field (IntegerField)
  - `author` field (ForeignKey to Author with related_name='books')
- ✅ Implemented proper `__str__` methods for both models
- ✅ Added comprehensive docstrings explaining model purpose and relationships
- ✅ Configured CASCADE deletion behavior
- ✅ Registered models in Django admin interface

**Models Defined (api/models.py):**

```python
class Author(models.Model):
    """Author model with one-to-many relationship to Books."""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model with foreign key to Author."""
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    def __str__(self):
        return self.title
```

**Migrations:**
- ✅ Created migration file: `api/migrations/0001_initial.py`
- ✅ Applied all migrations successfully
- ✅ Database tables created for both models

---

## Step 4: Create Custom Serializers ✅

**Completed Actions:**
- ✅ Created `BookSerializer` that serializes all fields of the Book model
- ✅ Created `AuthorSerializer` with:
  - `name` field
  - Nested `BookSerializer` for related books
- ✅ Implemented custom validation in `BookSerializer`:
  - `validate_publication_year` method prevents future years
  - Provides descriptive error messages with current year
- ✅ Used `many=True` for one-to-many relationship
- ✅ Used `read_only=True` for nested serialization

**Serializers Implemented (api/serializers.py):**

### BookSerializer
```python
class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model with custom validation."""
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """Ensures publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
```

### AuthorSerializer
```python
class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author with nested Book serialization."""
    
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
```

---

## Step 5: Document Model and Serializer Setup ✅

**Completed Actions:**
- ✅ Added detailed docstrings in `models.py` explaining:
  - Purpose of each model
  - Field descriptions
  - Relationship between Author and Book
  - Cascade deletion behavior
  - Related name usage
  
- ✅ Added comprehensive docstrings in `serializers.py` explaining:
  - Purpose of each serializer
  - Field descriptions
  - How nested relationships are handled
  - Validation logic and error messages
  - Example JSON output format
  - Usage of `many=True` and `read_only=True`

**Documentation Files:**
- ✅ Comprehensive `README.md` with:
  - Project overview
  - Setup instructions
  - Model descriptions
  - Serializer explanations
  - Testing guidelines
  - Example usage
  - Key features demonstrated
  - Next steps for extending the project

---

## Step 6: Implement and Test ✅

**Completed Actions:**

### Automated Testing
- ✅ Created comprehensive test script (`test_serializers.py`) that tests:
  1. Creating Author instances
  2. Creating Book instances with foreign key relationships
  3. Serializing individual books
  4. Serializing authors with nested books
  5. Validation with valid publication years (passes)
  6. Validation with future years (correctly fails)
  7. Reverse relationship queries (author.books.all())
  8. Serializing multiple authors with their books

### Test Results
All tests passed successfully:
```
✓ Authors created successfully
✓ Books created with author relationships
✓ BookSerializer serializes data correctly
✓ AuthorSerializer includes nested books
✓ Validation passes for valid years
✓ Validation correctly rejects future years
✓ Reverse relationships work as expected
✓ Multiple authors serialize with their books
```

### Admin Interface
- ✅ Registered both models in Django admin
- ✅ Configured admin list displays with relevant fields
- ✅ Added search and filter capabilities
- ✅ Models can be managed through admin interface

### Manual Testing
- ✅ Tested creating instances via Django shell
- ✅ Verified serialization output format
- ✅ Confirmed validation error messages
- ✅ Tested reverse relationships (author.books.all())

---

## Project Structure

```
advanced-api-project/
├── .gitignore                    # Git ignore file
├── README.md                     # Comprehensive documentation
├── manage.py                     # Django management script
├── test_serializers.py          # Test script
├── db.sqlite3                   # SQLite database
├── advanced_api_project/        # Project settings directory
│   ├── __init__.py
│   ├── settings.py              # ✅ Configured with REST framework
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── api/                         # API application
    ├── __init__.py
    ├── models.py                # ✅ Author and Book models
    ├── serializers.py           # ✅ Custom serializers with validation
    ├── admin.py                 # ✅ Admin configuration
    ├── apps.py
    ├── tests.py
    ├── views.py
    └── migrations/
        ├── __init__.py
        └── 0001_initial.py      # ✅ Initial migration
```

---

## Key Features Implemented

### 1. Model Relationships
- ✅ One-to-many relationship (Author → Books)
- ✅ Foreign key with CASCADE deletion
- ✅ Related name for reverse queries
- ✅ Proper `__str__` methods

### 2. Custom Serializers
- ✅ BookSerializer with all fields
- ✅ AuthorSerializer with nested books
- ✅ Custom validation logic
- ✅ Comprehensive documentation

### 3. Data Validation
- ✅ Publication year cannot be in future
- ✅ Descriptive error messages
- ✅ Current year comparison

### 4. Nested Serialization
- ✅ Books nested within Author
- ✅ Uses related_name='books'
- ✅ Read-only nested data
- ✅ Many-to-one relationship handling

### 5. Testing
- ✅ Automated test script
- ✅ All test cases pass
- ✅ Manual testing via Django shell
- ✅ Admin interface testing

---

## Repository Information

- **GitHub Repository:** Alx_DjangoLearnLab
- **Directory:** advanced-api-project
- **Branch:** master
- **Commit:** "Initial setup: Django project with custom serializers for Author and Book models"

---

## How to Verify

### 1. Run the test script:
```bash
cd advanced-api-project
python test_serializers.py
```

### 2. Test via Django shell:
```bash
python manage.py shell
```
```python
from api.models import Author, Book
from api.serializers import AuthorSerializer

author = Author.objects.create(name="Test Author")
book = Book.objects.create(title="Test Book", publication_year=2020, author=author)
serializer = AuthorSerializer(author)
print(serializer.data)
```

### 3. Access Django admin:
```bash
python manage.py createsuperuser  # Create admin user
python manage.py runserver         # Start server
# Navigate to http://127.0.0.1:8000/admin/
```

---

## Conclusion

✅ **All requirements for Task 0 have been successfully completed:**

1. ✅ Django and Django REST Framework installed
2. ✅ Project and app created with proper structure
3. ✅ Settings configured with REST framework
4. ✅ Author and Book models defined with proper relationships
5. ✅ Migrations created and applied
6. ✅ Custom serializers implemented with nested relationships
7. ✅ Custom validation added to prevent future publication years
8. ✅ Comprehensive documentation in models.py and serializers.py
9. ✅ Testing completed and verified
10. ✅ Project committed and pushed to GitHub

The project is ready for use and demonstrates advanced API development with Django REST Framework, including custom serializers, nested relationships, and data validation.
