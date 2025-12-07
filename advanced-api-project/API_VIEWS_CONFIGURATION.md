# API Views Configuration Documentation

## Overview

This document provides detailed information about how each view is configured in the Advanced API Project. The views are built using Django REST Framework's generic views, which provide standardized CRUD operations with minimal code.

## View Architecture

### Generic Views Used

The project implements five generic views from Django REST Framework:

1. **ListAPIView** - For listing all resources
2. **RetrieveAPIView** - For retrieving a single resource
3. **CreateAPIView** - For creating new resources
4. **UpdateAPIView** - For updating existing resources
5. **DestroyAPIView** - For deleting resources

### Base Configuration

All views inherit from `generics.GenericAPIView` and share these common configurations:

```python
queryset = Book.objects.all()
serializer_class = BookSerializer
```

## Individual View Configurations

### 1. BookListView (ListAPIView)

**File**: `api/views.py`

**Purpose**: Retrieve all books from the database

**Configuration**:
```python
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']
```

**Custom Settings**:
- **Permission Classes**: `AllowAny` - No authentication required
- **Filter Backends**: 
  - `SearchFilter` - Enables text search
  - `OrderingFilter` - Enables result ordering
- **Search Fields**: Can search by book title or author name
- **Ordering Fields**: Can order by title or publication_year
- **Default Ordering**: Results are ordered by title alphabetically

**HTTP Methods**: GET only

**URL Pattern**: `/api/books/`

**Query Parameters**:
- `?search=<term>` - Search for books
- `?ordering=title` - Order by title (ascending)
- `?ordering=-title` - Order by title (descending)
- `?ordering=publication_year` - Order by year

**Example Requests**:
```bash
# Get all books
GET /api/books/

# Search for books
GET /api/books/?search=Harry

# Order by publication year
GET /api/books/?ordering=publication_year

# Search and order combined
GET /api/books/?search=Potter&ordering=-publication_year
```

---

### 2. BookDetailView (RetrieveAPIView)

**File**: `api/views.py`

**Purpose**: Retrieve a single book by its primary key (ID)

**Configuration**:
```python
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
```

**Custom Settings**:
- **Permission Classes**: `AllowAny` - No authentication required
- **Lookup Field**: Uses default `pk` (primary key)

**HTTP Methods**: GET only

**URL Pattern**: `/api/books/<int:pk>/`

**URL Parameters**:
- `pk` (integer) - The ID of the book to retrieve

**Example Requests**:
```bash
# Get book with ID 1
GET /api/books/1/

# Get book with ID 42
GET /api/books/42/
```

**Response Codes**:
- `200 OK` - Book found and returned
- `404 Not Found` - Book with given ID doesn't exist

---

### 3. BookCreateView (CreateAPIView)

**File**: `api/views.py`

**Purpose**: Create a new book in the database

**Configuration**:
```python
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
```

**Custom Settings**:
- **Permission Classes**: `IsAuthenticated` - Requires user authentication
- **Custom Method**: `perform_create()` - Hook for additional logic before saving

**HTTP Methods**: POST only

**URL Pattern**: `/api/books/create/`

**Authentication Required**: Yes (Token or Session)

**Request Headers**:
```
Authorization: Token <your-auth-token>
Content-Type: application/json
```

**Request Body**:
```json
{
    "title": "Book Title",
    "publication_year": 2024,
    "author": 1
}
```

**Example Request**:
```bash
POST /api/books/create/
Headers:
  Authorization: Token abc123def456
  Content-Type: application/json
Body:
{
    "title": "The Great Gatsby",
    "publication_year": 1925,
    "author": 1
}
```

**Response Codes**:
- `201 Created` - Book successfully created
- `400 Bad Request` - Validation error (invalid data)
- `401 Unauthorized` - Not authenticated

**Validation Rules**:
- All fields are required
- `title` must be 200 characters or less
- `publication_year` cannot be in the future
- `author` must reference an existing author ID

**Custom Hooks**:

The `perform_create()` method can be extended to add custom logic:

```python
def perform_create(self, serializer):
    # Example: Set the user who created the book
    serializer.save(created_by=self.request.user)
    
    # Example: Send notification after creation
    book = serializer.save()
    send_notification(f"New book created: {book.title}")
```

---

### 4. BookUpdateView (UpdateAPIView)

**File**: `api/views.py`

**Purpose**: Update an existing book (full or partial update)

**Configuration**:
```python
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        serializer.save()
```

**Custom Settings**:
- **Permission Classes**: `IsAuthenticated` - Requires user authentication
- **Custom Method**: `perform_update()` - Hook for additional logic before saving
- **Lookup Field**: Uses default `pk` (primary key)

**HTTP Methods**: PUT, PATCH

**URL Pattern**: `/api/books/<int:pk>/update/`

**Authentication Required**: Yes (Token or Session)

**Request Headers**:
```
Authorization: Token <your-auth-token>
Content-Type: application/json
```

**PUT Request Body** (full update - all fields required):
```json
{
    "title": "Updated Title",
    "publication_year": 2024,
    "author": 1
}
```

**PATCH Request Body** (partial update - any subset of fields):
```json
{
    "title": "New Title"
}
```

**Example Requests**:
```bash
# Full update (PUT)
PUT /api/books/1/update/
Headers:
  Authorization: Token abc123def456
  Content-Type: application/json
Body:
{
    "title": "Updated Book",
    "publication_year": 2024,
    "author": 1
}

# Partial update (PATCH)
PATCH /api/books/1/update/
Headers:
  Authorization: Token abc123def456
  Content-Type: application/json
Body:
{
    "publication_year": 2025
}
```

**Response Codes**:
- `200 OK` - Book successfully updated
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Not authenticated
- `404 Not Found` - Book doesn't exist

**Validation Rules**:
- Same as CreateView for provided fields
- For PATCH: Only provided fields are validated
- For PUT: All fields are required

**Custom Hooks**:

The `perform_update()` method can be extended:

```python
def perform_update(self, serializer):
    # Example: Track who updated the book
    serializer.save(updated_by=self.request.user, updated_at=timezone.now())
    
    # Example: Log the update
    logger.info(f"Book {serializer.instance.id} updated by {self.request.user}")
```

---

### 5. BookDeleteView (DestroyAPIView)

**File**: `api/views.py`

**Purpose**: Delete a book from the database

**Configuration**:
```python
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
```

**Custom Settings**:
- **Permission Classes**: `IsAuthenticated` - Requires user authentication
- **Lookup Field**: Uses default `pk` (primary key)
- **Delete Type**: Hard delete (permanent removal)

**HTTP Methods**: DELETE only

**URL Pattern**: `/api/books/<int:pk>/delete/`

**Authentication Required**: Yes (Token or Session)

**Request Headers**:
```
Authorization: Token <your-auth-token>
```

**Example Request**:
```bash
DELETE /api/books/1/delete/
Headers:
  Authorization: Token abc123def456
```

**Response Codes**:
- `204 No Content` - Book successfully deleted
- `401 Unauthorized` - Not authenticated
- `404 Not Found` - Book doesn't exist

**Important Notes**:
- This is a **hard delete** - the book is permanently removed
- No request body is needed
- No response body is returned on success
- Consider implementing soft deletes for production

**Custom Hooks**:

The `perform_destroy()` method can be overridden:

```python
def perform_destroy(self, instance):
    # Example: Log deletion
    logger.warning(f"Book {instance.id} deleted by {self.request.user}")
    
    # Example: Archive instead of delete (soft delete)
    instance.is_deleted = True
    instance.save()
```

---

## Permission Classes

### Overview

The project uses Django REST Framework's built-in permission classes:

1. **AllowAny**: No restrictions - all users can access
2. **IsAuthenticated**: Only authenticated users can access

### Permission Implementation

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

# Used in views
permission_classes = [permissions.AllowAny]
permission_classes = [IsAuthenticated]
```

### Permission by View

| View | Permission | Authenticated Required | Unauthenticated Access |
|------|-----------|------------------------|------------------------|
| BookListView | AllowAny | No | Yes (Read-only) |
| BookDetailView | AllowAny | No | Yes (Read-only) |
| BookCreateView | IsAuthenticated | Yes | No |
| BookUpdateView | IsAuthenticated | Yes | No |
| BookDeleteView | IsAuthenticated | Yes | No |

### Custom Permission Classes

You can create custom permissions by extending `BasePermission`:

```python
from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    """
    Custom permission: Only the book's author can edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Write permissions only for the author
        return obj.author == request.user
```

---

## Serializer Integration

### BookSerializer

The views use `BookSerializer` for data validation and transformation:

```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """Ensure publication year is not in the future."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
```

### Validation Flow

1. **Request received** → View receives data
2. **Serializer instantiated** → View creates serializer with data
3. **Validation** → `serializer.is_valid()` runs validation
4. **Field validation** → Each field validated against type/constraints
5. **Custom validation** → `validate_<field>()` methods executed
6. **Save** → If valid, `serializer.save()` creates/updates object
7. **Response** → Serialized object returned to client

---

## URL Configuration

### API URLs (api/urls.py)

```python
from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

app_name = 'api'

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
```

### Main URLs (advanced_api_project/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

### URL Naming Convention

- **List/Create**: `books/` - Plural, no ID
- **Detail/Update/Delete**: `books/<pk>/` - Plural with ID
- **Named URLs**: Use for reverse lookups
  - `reverse('api:book-list')`
  - `reverse('api:book-detail', kwargs={'pk': 1})`

---

## Advanced Features

### 1. Filtering and Search

**SearchFilter** enables text search across specified fields:

```python
filter_backends = [filters.SearchFilter]
search_fields = ['title', 'author__name']  # Search in title or author's name
```

**Usage**:
```bash
GET /api/books/?search=Potter
GET /api/books/?search=Rowling
```

### 2. Ordering

**OrderingFilter** allows client-side result ordering:

```python
filter_backends = [filters.OrderingFilter]
ordering_fields = ['title', 'publication_year']
ordering = ['title']  # Default ordering
```

**Usage**:
```bash
GET /api/books/?ordering=title           # Ascending
GET /api/books/?ordering=-title          # Descending
GET /api/books/?ordering=publication_year
```

### 3. Pagination

Configured in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

**Usage**:
```bash
GET /api/books/?page=1
GET /api/books/?page=2
```

**Response Format**:
```json
{
    "count": 25,
    "next": "http://api.example.com/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

---

## Error Handling

### Standard Error Responses

**400 Bad Request** - Validation error:
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2024."
    ]
}
```

**401 Unauthorized** - Authentication required:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**404 Not Found** - Resource doesn't exist:
```json
{
    "detail": "Not found."
}
```

**500 Internal Server Error** - Server error:
```json
{
    "detail": "Internal server error."
}
```

---

## Best Practices Implemented

1. **DRY Principle**: Reusable generic views reduce code duplication
2. **Separation of Concerns**: Views handle HTTP, serializers handle data
3. **Clear Documentation**: Comprehensive docstrings in all views
4. **Consistent URLs**: RESTful URL patterns
5. **Proper Permissions**: Read/Write access separation
6. **Validation**: Data integrity through serializer validation
7. **HTTP Standards**: Correct status codes and methods

---

## Extension Points

### Adding Custom Behavior

Each generic view provides hooks for customization:

**CreateView**:
- `perform_create(serializer)` - Pre-save logic
- `get_serializer_class()` - Dynamic serializer selection
- `get_queryset()` - Dynamic queryset filtering

**UpdateView**:
- `perform_update(serializer)` - Pre-save logic
- `partial_update()` - PATCH handling

**DeleteView**:
- `perform_destroy(instance)` - Custom deletion logic

### Example: Adding Created By Field

```python
class BookCreateView(generics.CreateAPIView):
    # ... existing config ...
    
    def perform_create(self, serializer):
        # Automatically set the user who created the book
        serializer.save(created_by=self.request.user)
```

### Example: Soft Delete

```python
class BookDeleteView(generics.DestroyAPIView):
    # ... existing config ...
    
    def perform_destroy(self, instance):
        # Soft delete - mark as deleted instead of removing
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save()
```

---

## Testing Recommendations

### Unit Tests

```python
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'pass')
        
    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Test', 'publication_year': 2024, 'author': 1}
        response = self.client.post('/api/books/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

---

## Summary

This view configuration provides:
- ✅ Complete CRUD operations
- ✅ Proper authentication and permissions
- ✅ Data validation through serializers
- ✅ Filtering and search capabilities
- ✅ RESTful URL structure
- ✅ Comprehensive documentation
- ✅ Extension points for customization
- ✅ Error handling
- ✅ Best practices compliance

The architecture is maintainable, scalable, and follows Django REST Framework conventions.
