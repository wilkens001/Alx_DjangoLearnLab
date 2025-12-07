# Filtering, Searching, and Ordering Implementation

## Overview

This document details the implementation of advanced query capabilities for the Book API, including filtering, searching, and ordering functionality. These features enable API consumers to efficiently retrieve and organize book data based on various criteria.

## Implementation Details

### Dependencies

The implementation uses the following Django REST Framework components:

1. **DjangoFilterBackend** - Provides precise field-based filtering
2. **SearchFilter** - Enables text-based searching across multiple fields
3. **OrderingFilter** - Allows client-side result ordering

### Installation

Ensure `django-filter` is installed:

```bash
pip install django-filter
```

### Configuration

#### Settings (`advanced_api_project/settings.py`)

Added `django_filters` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_filters',  # For advanced filtering capabilities
    'api',
]
```

#### Views (`api/views.py`)

The `BookListView` has been enhanced with three filter backends:

```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    # Enable all three backends
    filter_backends = [
        DjangoFilterBackend,  # For filtering
        filters.SearchFilter,  # For searching
        filters.OrderingFilter  # For ordering
    ]
    
    # Configuration
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering
```

---

## Feature 1: Filtering

### Description

Filtering allows users to retrieve books that exactly match specified field values. This is useful for finding books by specific attributes.

### Configuration

```python
filter_backends = [DjangoFilterBackend]
filterset_fields = ['title', 'author', 'publication_year']
```

### Supported Filters

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `title` | String | Exact title match | `?title=The Hobbit` |
| `author` | Integer | Author ID | `?author=1` |
| `publication_year` | Integer | Publication year | `?publication_year=1997` |

### Usage Examples

#### Filter by Title

**Request:**
```bash
GET /api/books/?title=The Hobbit
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?title=The%20Hobbit"
```

**Expected Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "title": "The Hobbit",
            "publication_year": 1937,
            "author": 2
        }
    ]
}
```

#### Filter by Author

**Request:**
```bash
GET /api/books/?author=1
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"
```

**Description:** Returns all books written by the author with ID 1.

#### Filter by Publication Year

**Request:**
```bash
GET /api/books/?publication_year=1997
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?publication_year=1997"
```

**Description:** Returns all books published in 1997.

#### Multiple Filters (Combined)

**Request:**
```bash
GET /api/books/?author=1&publication_year=1997
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&publication_year=1997"
```

**Description:** Returns books by author 1 published in 1997.

### Python Example

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

# Filter by author
response = requests.get(BASE_URL, params={'author': 1})
print(response.json())

# Filter by publication year
response = requests.get(BASE_URL, params={'publication_year': 1997})
print(response.json())

# Combined filters
response = requests.get(BASE_URL, params={
    'author': 1,
    'publication_year': 1997
})
print(response.json())
```

---

## Feature 2: Searching

### Description

Searching provides text-based, partial matching across specified fields. Unlike filtering, searching finds records that contain the search term (case-insensitive).

### Configuration

```python
filter_backends = [filters.SearchFilter]
search_fields = ['title', 'author__name']
```

### Supported Search Fields

| Field | Description |
|-------|-------------|
| `title` | Searches in book titles |
| `author__name` | Searches in author names (related field) |

### Usage Examples

#### Search by Title

**Request:**
```bash
GET /api/books/?search=Potter
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter"
```

**Expected Response:**
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
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": 1
        }
    ]
}
```

**Description:** Returns all books with "Potter" in the title.

#### Search by Author Name

**Request:**
```bash
GET /api/books/?search=Rowling
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Rowling"
```

**Description:** Returns all books by authors whose name contains "Rowling".

#### Search Multiple Words

**Request:**
```bash
GET /api/books/?search=Harry Stone
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Harry%20Stone"
```

**Description:** Searches for books containing "Harry Stone" in title or author name.

### Python Example

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

# Search for books with "Potter" in title or author
response = requests.get(BASE_URL, params={'search': 'Potter'})
print(response.json())

# Search for books by author name
response = requests.get(BASE_URL, params={'search': 'Rowling'})
print(response.json())
```

### Search Behavior

- **Case-insensitive**: "potter", "Potter", "POTTER" all match
- **Partial matching**: "Pot" matches "Potter"
- **Multiple fields**: Searches across both title and author name
- **Word boundaries**: Searches for terms anywhere in the field

---

## Feature 3: Ordering

### Description

Ordering allows users to sort results by specified fields in ascending or descending order.

### Configuration

```python
filter_backends = [filters.OrderingFilter]
ordering_fields = ['title', 'publication_year']
ordering = ['title']  # Default ordering
```

### Supported Ordering Fields

| Field | Description | Ascending | Descending |
|-------|-------------|-----------|------------|
| `title` | Book title | `?ordering=title` | `?ordering=-title` |
| `publication_year` | Publication year | `?ordering=publication_year` | `?ordering=-publication_year` |

### Usage Examples

#### Order by Title (Ascending)

**Request:**
```bash
GET /api/books/?ordering=title
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=title"
```

**Description:** Returns books ordered alphabetically by title (A-Z).

#### Order by Title (Descending)

**Request:**
```bash
GET /api/books/?ordering=-title
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-title"
```

**Description:** Returns books ordered reverse alphabetically by title (Z-A).

#### Order by Publication Year (Ascending)

**Request:**
```bash
GET /api/books/?ordering=publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=publication_year"
```

**Description:** Returns books ordered by publication year (oldest first).

#### Order by Publication Year (Descending)

**Request:**
```bash
GET /api/books/?ordering=-publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

**Description:** Returns books ordered by publication year (newest first).

#### Multiple Ordering Fields

**Request:**
```bash
GET /api/books/?ordering=author,publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=author,publication_year"
```

**Description:** Orders by author first, then by publication year within each author.

### Python Example

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

# Order by title (ascending)
response = requests.get(BASE_URL, params={'ordering': 'title'})
print(response.json())

# Order by title (descending)
response = requests.get(BASE_URL, params={'ordering': '-title'})
print(response.json())

# Order by publication year (newest first)
response = requests.get(BASE_URL, params={'ordering': '-publication_year'})
print(response.json())
```

### Default Ordering

If no ordering parameter is provided, results are ordered by title (ascending) by default:

```python
ordering = ['title']  # Default ordering
```

---

## Combined Usage

### Filtering + Searching + Ordering

You can combine all three features in a single request:

#### Example 1: Search and Order

**Request:**
```bash
GET /api/books/?search=Potter&ordering=-publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter&ordering=-publication_year"
```

**Description:** Search for books containing "Potter" and order by newest first.

#### Example 2: Filter and Order

**Request:**
```bash
GET /api/books/?author=1&ordering=publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&ordering=publication_year"
```

**Description:** Get books by author 1, ordered by publication year (oldest first).

#### Example 3: Filter, Search, and Order

**Request:**
```bash
GET /api/books/?author=1&search=Harry&ordering=-publication_year
```

**curl:**
```bash
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&search=Harry&ordering=-publication_year"
```

**Description:** Get books by author 1 containing "Harry" in title, ordered newest first.

### Python Example - Combined

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

# Complex query: Filter by author, search for "Harry", order by year
response = requests.get(BASE_URL, params={
    'author': 1,
    'search': 'Harry',
    'ordering': '-publication_year'
})

print(f"Status Code: {response.status_code}")
print(f"Results: {response.json()}")
```

---

## Testing

### Manual Testing with curl

#### Test 1: Basic Filtering

```bash
# Test filtering by author
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"

# Test filtering by publication year
curl -X GET "http://127.0.0.1:8000/api/books/?publication_year=1997"

# Test filtering by title
curl -X GET "http://127.0.0.1:8000/api/books/?title=The%20Hobbit"
```

#### Test 2: Search Functionality

```bash
# Test search by title keyword
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter"

# Test search by author name
curl -X GET "http://127.0.0.1:8000/api/books/?search=Rowling"

# Test search with multiple words
curl -X GET "http://127.0.0.1:8000/api/books/?search=Harry%20Potter"
```

#### Test 3: Ordering

```bash
# Test ascending order by title
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=title"

# Test descending order by title
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-title"

# Test ascending order by year
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=publication_year"

# Test descending order by year
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

#### Test 4: Combined Features

```bash
# Filter and order
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&ordering=-publication_year"

# Search and order
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter&ordering=publication_year"

# Filter, search, and order
curl -X GET "http://127.0.0.1:8000/api/books/?author=1&search=Harry&ordering=-publication_year"
```

### Testing with Postman

1. **Open Postman** and create a new request
2. **Set Method** to GET
3. **Enter URL**: `http://127.0.0.1:8000/api/books/`
4. **Go to Params tab** and add query parameters:

| Key | Value | Description |
|-----|-------|-------------|
| author | 1 | Filter by author |
| publication_year | 1997 | Filter by year |
| search | Potter | Search term |
| ordering | -publication_year | Order by year (desc) |

5. **Click Send** and verify the response

### Automated Test Script

Create `test_filtering.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/books/"

def test_filtering():
    print("\n=== Testing Filtering ===")
    
    # Test 1: Filter by author
    print("\n1. Filter by author (author=1):")
    response = requests.get(BASE_URL, params={'author': 1})
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test 2: Filter by year
    print("\n2. Filter by publication year (publication_year=1997):")
    response = requests.get(BASE_URL, params={'publication_year': 1997})
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
def test_searching():
    print("\n=== Testing Searching ===")
    
    # Test 1: Search by keyword
    print("\n1. Search for 'Potter':")
    response = requests.get(BASE_URL, params={'search': 'Potter'})
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    # Test 2: Search by author name
    print("\n2. Search for 'Rowling':")
    response = requests.get(BASE_URL, params={'search': 'Rowling'})
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")

def test_ordering():
    print("\n=== Testing Ordering ===")
    
    # Test 1: Order by title
    print("\n1. Order by title (ascending):")
    response = requests.get(BASE_URL, params={'ordering': 'title'})
    print(f"Status: {response.status_code}")
    titles = [book['title'] for book in response.json()['results']]
    print(f"First 3 titles: {titles[:3]}")
    
    # Test 2: Order by year (descending)
    print("\n2. Order by year (descending):")
    response = requests.get(BASE_URL, params={'ordering': '-publication_year'})
    print(f"Status: {response.status_code}")
    years = [book['publication_year'] for book in response.json()['results']]
    print(f"First 3 years: {years[:3]}")

def test_combined():
    print("\n=== Testing Combined Features ===")
    
    print("\n1. Filter by author + Order by year:")
    response = requests.get(BASE_URL, params={
        'author': 1,
        'ordering': '-publication_year'
    })
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")
    
    print("\n2. Search + Order:")
    response = requests.get(BASE_URL, params={
        'search': 'Potter',
        'ordering': 'publication_year'
    })
    print(f"Status: {response.status_code}")
    print(f"Count: {response.json()['count']}")

if __name__ == "__main__":
    print("Starting API Tests...")
    test_filtering()
    test_searching()
    test_ordering()
    test_combined()
    print("\n=== All Tests Completed ===")
```

Run the tests:
```bash
python test_filtering.py
```

---

## Query Parameter Reference

### Quick Reference Table

| Feature | Parameter | Example | Description |
|---------|-----------|---------|-------------|
| **Filtering** | `title` | `?title=The Hobbit` | Exact title match |
| | `author` | `?author=1` | Filter by author ID |
| | `publication_year` | `?publication_year=1997` | Filter by year |
| **Searching** | `search` | `?search=Potter` | Search in title and author |
| **Ordering** | `ordering` | `?ordering=title` | Order by title (asc) |
| | `ordering` | `?ordering=-title` | Order by title (desc) |
| | `ordering` | `?ordering=publication_year` | Order by year (asc) |
| | `ordering` | `?ordering=-publication_year` | Order by year (desc) |

### URL Construction Examples

```
# Basic filtering
/api/books/?author=1
/api/books/?publication_year=1997

# Searching
/api/books/?search=Potter

# Ordering
/api/books/?ordering=title
/api/books/?ordering=-publication_year

# Combined
/api/books/?author=1&search=Harry&ordering=-publication_year
```

---

## Implementation Benefits

### For API Consumers

1. **Flexibility**: Query data exactly as needed
2. **Efficiency**: Reduce data transfer by filtering server-side
3. **User Experience**: Enable intuitive data exploration
4. **Performance**: Server-side filtering is faster than client-side

### For Developers

1. **Maintainability**: Built-in DRF features require minimal code
2. **Consistency**: Standard query parameters across all endpoints
3. **Extensibility**: Easy to add more filterable fields
4. **Documentation**: Self-documenting through API browsable interface

---

## Advanced Configuration

### Custom Filter Classes

For more complex filtering logic, create custom filter classes:

```python
from django_filters import rest_framework as filters

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    min_year = filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    
    class Meta:
        model = Book
        fields = ['title', 'author']

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
```

### Custom Search Behavior

Customize search with different lookup types:

```python
from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        # Customize search fields dynamically
        return ['title', 'author__name', 'author__bio']

class BookListView(generics.ListAPIView):
    filter_backends = [CustomSearchFilter]
    search_fields = ['title', 'author__name']
```

---

## Troubleshooting

### Common Issues

**Issue 1: Filtering not working**
- **Cause**: `django-filter` not installed
- **Solution**: `pip install django-filter` and add to `INSTALLED_APPS`

**Issue 2: Search returns no results**
- **Cause**: Case-sensitive database or incorrect field names
- **Solution**: Use `icontains` lookup or check field names

**Issue 3: Ordering not applied**
- **Cause**: Missing `OrderingFilter` in `filter_backends`
- **Solution**: Add `filters.OrderingFilter` to backend list

**Issue 4: Invalid ordering field error**
- **Cause**: Ordering field not in `ordering_fields`
- **Solution**: Add the field to `ordering_fields` list

---

## Summary

This implementation provides comprehensive query capabilities for the Book API:

✅ **Filtering**: Precise field-based filtering (title, author, year)  
✅ **Searching**: Text-based searching across title and author  
✅ **Ordering**: Flexible result ordering (ascending/descending)  
✅ **Combined**: All features work together seamlessly  
✅ **Documented**: Comprehensive documentation and examples  
✅ **Tested**: Tested with curl, Postman, and Python scripts  

The implementation follows Django REST Framework best practices and provides an excellent user experience for API consumers.
