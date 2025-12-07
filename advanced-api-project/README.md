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
   pip install django djangorestframework django-filter
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

## API Views and Endpoints

The project now includes a complete set of generic views for CRUD operations on the Book model, with proper authentication and permission handling.

### Available Views

#### 1. BookListView (ListView)
**Purpose**: Retrieve all books in the database

**Endpoint**: `GET /api/books/`

**Permissions**: AllowAny (read-only access for everyone)

**Features**:
- Returns a list of all Book objects
- **Advanced Filtering**: Filter by title, author, and publication_year
- **Text Search**: Search across title and author name fields
- **Flexible Ordering**: Order by title and publication_year (ascending/descending)
- Default ordering by title

**Basic Request**:
```bash
curl -X GET http://127.0.0.1:8000/api/books/
```

**Filtering Examples**:
```bash
# Filter by author
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"

# Filter by publication year
curl -X GET "http://127.0.0.1:8000/api/books/?publication_year=1997"

# Multiple filters
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&publication_year=1997"
```

**Search Examples**:
```bash
# Search for books containing "Potter"
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter"

# Search by author name
curl -X GET "http://127.0.0.1:8000/api/books/?search=Rowling"
```

**Ordering Examples**:
```bash
# Order by title (ascending)
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=title"

# Order by publication year (descending - newest first)
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

**Combined Query Example**:
```bash
# Search, filter, and order combined
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter&author=1&ordering=-publication_year"
```

**Example Response**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Harry Potter and the Philosopher's Stone",
            "publication_year": 1997,
            "author": 1
        },
        {
            "id": 2,
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": 2
        }
    ]
}
```

**Query Parameters Reference**:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `author` | Integer | Filter by author ID | `?author=1` |
| `title` | String | Filter by exact title | `?title=The Hobbit` |
| `publication_year` | Integer | Filter by year | `?publication_year=1997` |
| `search` | String | Search in title and author name | `?search=Potter` |
| `ordering` | String | Order results (use `-` for descending) | `?ordering=-publication_year` |

📚 **For detailed documentation on filtering, searching, and ordering, see [FILTERING_SEARCHING_ORDERING.md](FILTERING_SEARCHING_ORDERING.md)**

#### 2. BookDetailView (DetailView)
**Purpose**: Retrieve a single book by its ID

**Endpoint**: `GET /api/books/<int:pk>/`

**Permissions**: AllowAny (read-only access for everyone)

**URL Parameters**:
- `pk` (required): The primary key (ID) of the book

**Example Request**:
```bash
curl -X GET http://127.0.0.1:8000/api/books/1/
```

**Example Response**:
```json
{
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
}
```

**Error Responses**:
- `404 Not Found`: If book with the given ID doesn't exist

#### 3. BookCreateView (CreateView)
**Purpose**: Create a new book

**Endpoint**: `POST /api/books/create/`

**Permissions**: IsAuthenticated (requires authentication)

**Request Headers**:
```
Authorization: Token <your-auth-token>
Content-Type: application/json
```

**Request Body**:
```json
{
    "title": "New Book Title",
    "publication_year": 2024,
    "author": 1
}
```

**Example Request**:
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token <your-auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Book",
    "publication_year": 2024,
    "author": 1
  }'
```

**Success Response** (`201 Created`):
```json
{
    "id": 3,
    "title": "New Book",
    "publication_year": 2024,
    "author": 1
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors (e.g., future publication year)
- `401 Unauthorized`: User is not authenticated

**Validation Rules**:
- `title`: Required, max 200 characters
- `publication_year`: Required, cannot be in the future
- `author`: Required, must be a valid author ID

#### 4. BookUpdateView (UpdateView)
**Purpose**: Update an existing book (full or partial update)

**Endpoints**: 
- `PUT /api/books/<int:pk>/update/` (full update)
- `PATCH /api/books/<int:pk>/update/` (partial update)

**Permissions**: IsAuthenticated (requires authentication)

**URL Parameters**:
- `pk` (required): The primary key (ID) of the book to update

**Request Headers**:
```
Authorization: Token <your-auth-token>
Content-Type: application/json
```

**PUT Request Body** (all fields required):
```json
{
    "title": "Updated Book Title",
    "publication_year": 2024,
    "author": 1
}
```

**PATCH Request Body** (partial update, any subset):
```json
{
    "title": "Updated Title"
}
```

**Example Request**:
```bash
# Full update (PUT)
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token <your-auth-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Book",
    "publication_year": 2024,
    "author": 1
  }'

# Partial update (PATCH)
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token <your-auth-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title"}'
```

**Success Response** (`200 OK`):
```json
{
    "id": 1,
    "title": "Updated Book",
    "publication_year": 2024,
    "author": 1
}
```

**Error Responses**:
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: User is not authenticated
- `404 Not Found`: Book with given ID doesn't exist

#### 5. BookDeleteView (DeleteView)
**Purpose**: Delete a book from the database

**Endpoint**: `DELETE /api/books/<int:pk>/delete/`

**Permissions**: IsAuthenticated (requires authentication)

**URL Parameters**:
- `pk` (required): The primary key (ID) of the book to delete

**Request Headers**:
```
Authorization: Token <your-auth-token>
```

**Example Request**:
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token <your-auth-token>"
```

**Success Response** (`204 No Content`):
```
(No content returned)
```

**Error Responses**:
- `401 Unauthorized`: User is not authenticated
- `404 Not Found`: Book with given ID doesn't exist

**Note**: This performs a hard delete. The operation is permanent and cannot be undone.

### Permission Structure

The API implements a two-tier permission system:

1. **Read Operations** (ListView, DetailView):
   - Permission Class: `AllowAny`
   - Access: Both authenticated and unauthenticated users
   - Operations: GET requests only
   - Use Case: Public access to book information

2. **Write Operations** (CreateView, UpdateView, DeleteView):
   - Permission Class: `IsAuthenticated`
   - Access: Authenticated users only
   - Operations: POST, PUT, PATCH, DELETE
   - Use Case: Controlled modification of book data

### Custom View Features

#### Form Submission and Validation
- All create and update views automatically handle form submission
- Data validation is performed through the `BookSerializer`
- Custom validation ensures publication_year is not in the future
- Detailed error messages are returned for validation failures

#### perform_create() and perform_update() Methods
These custom methods are hooks provided by DRF that execute after validation but before saving:

```python
def perform_create(self, serializer):
    """Custom logic during creation"""
    serializer.save()

def perform_update(self, serializer):
    """Custom logic during updates"""
    serializer.save()
```

**Use Cases**:
- Setting additional fields (e.g., created_by, updated_by)
- Performing side effects (e.g., sending notifications)
- Adding business logic before saving
- Logging changes

#### Filtering and Ordering
The `BookListView` includes:
- **Filtering**: Filter by title, author, or publication_year
- **Ordering**: Sort by title or publication_year
- **Default Ordering**: Books are ordered by title by default

**Example with Filters**:
```bash
# Filter by author
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"

# Filter by publication year
curl -X GET "http://127.0.0.1:8000/api/books/?publication_year=1997"

# Order by publication year
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=publication_year"
```

### Testing the API

#### Using Postman

1. **Install Postman** from https://www.postman.com/

2. **Test GET Requests** (no authentication needed):
   - Set method to GET
   - URL: `http://127.0.0.1:8000/api/books/`
   - Click Send

3. **Test POST/PUT/PATCH/DELETE** (authentication required):
   - First, create a user and get an auth token
   - Set method (POST/PUT/PATCH/DELETE)
   - URL: `http://127.0.0.1:8000/api/books/create/`
   - Headers: Add `Authorization: Token <your-token>`
   - Body: Select "raw" and "JSON", then add your data
   - Click Send

#### Using curl

```bash
# List all books (no auth required)
curl -X GET http://127.0.0.1:8000/api/books/

# Get a specific book (no auth required)
curl -X GET http://127.0.0.1:8000/api/books/1/

# Create a book (requires auth)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "publication_year": 2024, "author": 1}'

# Update a book (requires auth)
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "publication_year": 2024, "author": 1}'

# Delete a book (requires auth)
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token <your-token>"
```

#### Setting Up Authentication

To test authenticated endpoints, you need to:

1. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

2. **Install DRF Token Authentication** (if not already configured):
   Update `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework.authtoken',
   ]
   
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
   }
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create a token** (Django shell):
   ```python
   from django.contrib.auth.models import User
   from rest_framework.authtoken.models import Token
   
   user = User.objects.get(username='your_username')
   token = Token.objects.create(user=user)
   print(token.key)
   ```

### URL Pattern Configuration

All API endpoints are configured in `api/urls.py` and included in the main project URLs with the `/api/` prefix:

```python
# Main urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# api/urls.py
urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
```

### View Architecture

The project uses Django REST Framework's **Generic Views**, which provide:

1. **Pre-built Functionality**: Common CRUD operations out of the box
2. **Consistent Behavior**: Standardized responses and error handling
3. **Extensibility**: Easy to customize through method overrides
4. **DRY Principle**: Minimal code repetition
5. **Best Practices**: Built-in support for permissions, pagination, filtering

**Generic View Hierarchy**:
```
GenericAPIView (base)
├── ListAPIView (BookListView)
├── RetrieveAPIView (BookDetailView)
├── CreateAPIView (BookCreateView)
├── UpdateAPIView (BookUpdateView)
└── DestroyAPIView (BookDeleteView)
```

## Testing

The project includes comprehensive unit tests for all API endpoints, covering CRUD operations, filtering, searching, ordering, authentication, and permissions.

### Running Tests

```bash
# Run all tests
python manage.py test api

# Run with verbose output
python manage.py test api --verbosity=2

# Run specific test class
python manage.py test api.test_views.BookAPITestCase
```

### Test Coverage

| Category | Tests | Description |
|----------|-------|-------------|
| **CRUD Operations** | 11 | Create, Read, Update, Delete |
| **Filtering** | 5 | Filter by author, title, year |
| **Searching** | 5 | Search in titles and authors |
| **Ordering** | 5 | Order by title and year |
| **Permissions** | 8 | Authentication and access control |
| **Combined Features** | 3 | Multiple features together |
| **TOTAL** | **37** | **Complete coverage** |

### Expected Output

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................
----------------------------------------------------------------------
Ran 37 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

### Test Documentation

For comprehensive testing documentation, see:
- 📋 [TESTING_DOCUMENTATION.md](TESTING_DOCUMENTATION.md) - Complete testing guide
- ⚡ [TEST_COMMANDS.md](TEST_COMMANDS.md) - Quick command reference

### What's Tested

✅ **CRUD Operations**
- Creating books (authenticated users only)
- Reading books (public access)
- Updating books (authenticated users only)
- Deleting books (authenticated users only)
- Data validation (future publication year rejection)

✅ **Filtering**
- Filter by author ID
- Filter by publication year
- Filter by title
- Multiple filters combined

✅ **Searching**
- Search in book titles
- Search in author names
- Case-insensitive search
- Partial matching

✅ **Ordering**
- Order by title (A-Z and Z-A)
- Order by publication year (oldest/newest first)
- Default ordering

✅ **Permissions & Security**
- Unauthenticated read access (allowed)
- Authenticated write access (required)
- Token authentication
- Invalid token rejection
- Permission denial for unauthorized users

✅ **Combined Features**
- Filter + Order
- Search + Order
- Filter + Search + Order

### Next Steps

To further extend this project, consider:

1. **Adding more endpoints**:
   - Author CRUD endpoints
   - Combined list-create views
   - Bulk operations

2. **Enhancing security**:
   - Object-level permissions
   - Rate limiting
   - API versioning

3. **Improving functionality**:
   - Advanced filtering with django-filter
   - Custom pagination classes
   - API throttling

4. **Expanding tests**:
   - Integration tests
   - Performance tests
   - Load testing
   - Test coverage reports

5. **Documentation**:
   - API documentation with Swagger/OpenAPI
   - Interactive API browser
   - Postman collections

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [DRF Generic Views](https://www.django-rest-framework.org/api-guide/generic-views/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [DRF Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [DRF Relations](https://www.django-rest-framework.org/api-guide/relations/)
