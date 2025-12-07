# Unit Testing Documentation for Django REST Framework API

## Overview

This document provides comprehensive documentation for the unit tests implemented for the Book API in the advanced-api-project. The tests cover CRUD operations, filtering, searching, ordering, authentication, and permission controls.

## Table of Contents

1. [Testing Strategy](#testing-strategy)
2. [Test Suite Structure](#test-suite-structure)
3. [Running Tests](#running-tests)
4. [Test Cases](#test-cases)
5. [Understanding Test Results](#understanding-test-results)
6. [Continuous Testing](#continuous-testing)

---

## Testing Strategy

### Goals

Our testing strategy aims to:

1. **Ensure Correctness**: Verify that all API endpoints return correct data and status codes
2. **Validate Security**: Test authentication and permission controls
3. **Verify Features**: Confirm filtering, searching, and ordering work as expected
4. **Prevent Regressions**: Catch bugs early before they reach production
5. **Document Behavior**: Tests serve as executable documentation

### Testing Framework

- **Framework**: Django's built-in test framework (extends Python's `unittest`)
- **API Testing**: Django REST Framework's `APITestCase` and `APIClient`
- **Test Database**: Separate test database (auto-created and destroyed)
- **Isolation**: Each test method is independent and isolated

### What We Test

✅ **CRUD Operations**
- Creating books (authenticated)
- Reading books (unauthenticated)
- Updating books (authenticated)
- Deleting books (authenticated)

✅ **Filtering**
- Filter by author
- Filter by title
- Filter by publication year
- Multiple filters combined

✅ **Searching**
- Search in book titles
- Search in author names
- Case-insensitive searching
- Partial matching

✅ **Ordering**
- Order by title (ascending/descending)
- Order by publication year (ascending/descending)
- Default ordering

✅ **Permissions & Authentication**
- Unauthenticated read access
- Authenticated write access
- Permission denial for unauthenticated writes
- Token authentication
- Invalid token handling

✅ **Combined Features**
- Filter + Order
- Search + Order
- Filter + Search + Order

---

## Test Suite Structure

### Test File Location

```
advanced-api-project/
└── api/
    └── test_views.py
```

### Test Classes

Our test suite is organized into six test classes:

#### 1. **BookAPITestCase**
Tests basic CRUD operations on the Book API.

**Tests:**
- `test_list_books()` - List all books
- `test_retrieve_book()` - Get single book
- `test_retrieve_nonexistent_book()` - 404 for missing book
- `test_create_book_authenticated()` - Create with auth
- `test_create_book_unauthenticated()` - Create without auth (denied)
- `test_create_book_invalid_data()` - Validation errors
- `test_update_book_authenticated()` - Update with auth (PUT)
- `test_partial_update_book_authenticated()` - Partial update (PATCH)
- `test_update_book_unauthenticated()` - Update without auth (denied)
- `test_delete_book_authenticated()` - Delete with auth
- `test_delete_book_unauthenticated()` - Delete without auth (denied)

**Total Tests: 11**

#### 2. **BookFilteringTestCase**
Tests filtering functionality.

**Tests:**
- `test_filter_by_author()` - Filter by author ID
- `test_filter_by_publication_year()` - Filter by year
- `test_filter_by_title()` - Filter by exact title
- `test_filter_multiple_criteria()` - Multiple filters
- `test_filter_no_results()` - Empty results

**Total Tests: 5**

#### 3. **BookSearchingTestCase**
Tests search functionality.

**Tests:**
- `test_search_by_title()` - Search in titles
- `test_search_by_author_name()` - Search in author names
- `test_search_case_insensitive()` - Case-insensitive search
- `test_search_partial_match()` - Partial matching
- `test_search_no_results()` - Empty results

**Total Tests: 5**

#### 4. **BookOrderingTestCase**
Tests ordering functionality.

**Tests:**
- `test_default_ordering()` - Default sort by title
- `test_order_by_title_ascending()` - A-Z order
- `test_order_by_title_descending()` - Z-A order
- `test_order_by_year_ascending()` - Oldest first
- `test_order_by_year_descending()` - Newest first

**Total Tests: 5**

#### 5. **BookPermissionsTestCase**
Tests authentication and permission controls.

**Tests:**
- `test_unauthenticated_read_access()` - Read without auth (allowed)
- `test_authenticated_create_access()` - Create with auth
- `test_unauthenticated_create_denied()` - Create without auth (denied)
- `test_authenticated_update_access()` - Update with auth
- `test_unauthenticated_update_denied()` - Update without auth (denied)
- `test_authenticated_delete_access()` - Delete with auth
- `test_unauthenticated_delete_denied()` - Delete without auth (denied)
- `test_invalid_token_denied()` - Invalid token rejected

**Total Tests: 8**

#### 6. **BookCombinedFeaturesTestCase**
Tests combined features (filter + search + order).

**Tests:**
- `test_filter_and_order()` - Filter + Order
- `test_search_and_order()` - Search + Order
- `test_filter_search_and_order()` - All three combined

**Total Tests: 3**

### Total Test Count: **37 Tests**

---

## Running Tests

### Prerequisites

1. **Ensure the project is set up**:
   ```bash
   cd advanced-api-project
   pip install django djangorestframework django-filter
   python manage.py migrate
   ```

2. **Create a test user (optional, auto-created by tests)**:
   Tests automatically create test users and data

### Run All Tests

```bash
python manage.py test api
```

**Expected Output:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................
----------------------------------------------------------------------
Ran 37 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

### Run Specific Test Class

```bash
# Run only CRUD tests
python manage.py test api.test_views.BookAPITestCase

# Run only filtering tests
python manage.py test api.test_views.BookFilteringTestCase

# Run only permission tests
python manage.py test api.test_views.BookPermissionsTestCase
```

### Run Specific Test Method

```bash
# Run a single test
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated
```

### Run with Verbosity

```bash
# Verbose output (shows each test name)
python manage.py test api --verbosity=2

# Very verbose (shows all details)
python manage.py test api --verbosity=3
```

### Keep Test Database

```bash
# Keep database for inspection after tests
python manage.py test api --keepdb
```

### Run Tests in Parallel

```bash
# Run tests in parallel (faster for large test suites)
python manage.py test api --parallel
```

---

## Test Cases

### Detailed Test Case Documentation

#### CRUD Operations Tests

##### 1. test_list_books()

**Purpose**: Verify that the list endpoint returns all books

**Endpoint**: `GET /api/books/`

**Authentication**: Not required

**Test Steps:**
1. Create 3 test books in setUp()
2. Make GET request to `/api/books/`
3. Verify status code is 200 OK
4. Verify response contains all 3 books

**Expected Result:**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [...]
}
```

**Status Code**: 200 OK

---

##### 2. test_retrieve_book()

**Purpose**: Verify retrieving a single book by ID

**Endpoint**: `GET /api/books/{id}/`

**Authentication**: Not required

**Test Steps:**
1. Create test book with known ID
2. Make GET request to `/api/books/{id}/`
3. Verify status code is 200 OK
4. Verify response contains correct book data

**Expected Result:**
```json
{
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
}
```

**Status Code**: 200 OK

---

##### 3. test_create_book_authenticated()

**Purpose**: Verify authenticated users can create books

**Endpoint**: `POST /api/books/create/`

**Authentication**: Required (Token)

**Test Steps:**
1. Authenticate with valid token
2. Send POST request with book data
3. Verify status code is 201 CREATED
4. Verify book is saved in database
5. Verify response contains created book

**Request Body:**
```json
{
    "title": "New Test Book",
    "publication_year": 2024,
    "author": 1
}
```

**Expected Result:**
```json
{
    "id": 4,
    "title": "New Test Book",
    "publication_year": 2024,
    "author": 1
}
```

**Status Code**: 201 CREATED

---

##### 4. test_create_book_unauthenticated()

**Purpose**: Verify unauthenticated users cannot create books

**Endpoint**: `POST /api/books/create/`

**Authentication**: Not provided

**Test Steps:**
1. Send POST request without authentication
2. Verify status code is 401 UNAUTHORIZED
3. Verify book is NOT created in database

**Expected Result:**
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Status Code**: 401 UNAUTHORIZED

---

##### 5. test_create_book_invalid_data()

**Purpose**: Verify validation works (future publication year)

**Endpoint**: `POST /api/books/create/`

**Authentication**: Required

**Test Steps:**
1. Authenticate with valid token
2. Send POST with future publication year
3. Verify status code is 400 BAD REQUEST
4. Verify validation error is returned

**Request Body:**
```json
{
    "title": "Future Book",
    "publication_year": 3000,
    "author": 1
}
```

**Expected Result:**
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2024."
    ]
}
```

**Status Code**: 400 BAD REQUEST

---

#### Filtering Tests

##### 6. test_filter_by_author()

**Purpose**: Verify filtering by author works

**Endpoint**: `GET /api/books/?author={id}`

**Test Steps:**
1. Create books by different authors
2. Filter by specific author ID
3. Verify only books by that author are returned

**Example Request:**
```bash
GET /api/books/?author=1
```

**Verification:**
- All returned books have `author` field equal to 1
- Count matches expected number

---

##### 7. test_filter_by_publication_year()

**Purpose**: Verify filtering by year works

**Endpoint**: `GET /api/books/?publication_year={year}`

**Test Steps:**
1. Create books with different years
2. Filter by specific year
3. Verify only books from that year are returned

**Example Request:**
```bash
GET /api/books/?publication_year=1997
```

---

#### Searching Tests

##### 8. test_search_by_title()

**Purpose**: Verify searching in book titles works

**Endpoint**: `GET /api/books/?search={keyword}`

**Test Steps:**
1. Create books with different titles
2. Search for keyword
3. Verify results contain keyword in title

**Example Request:**
```bash
GET /api/books/?search=Potter
```

**Verification:**
- All results contain "Potter" in title
- Search is case-insensitive

---

##### 9. test_search_case_insensitive()

**Purpose**: Verify search is case-insensitive

**Test Steps:**
1. Search with lowercase keyword
2. Search with uppercase keyword
3. Verify both return same results

**Example:**
```bash
GET /api/books/?search=potter  # lowercase
GET /api/books/?search=POTTER  # uppercase
```

**Expected**: Same number of results

---

#### Ordering Tests

##### 10. test_order_by_title_ascending()

**Purpose**: Verify ordering by title (A-Z) works

**Endpoint**: `GET /api/books/?ordering=title`

**Test Steps:**
1. Create books with different titles
2. Order by title (ascending)
3. Verify results are in alphabetical order

**Verification:**
```python
titles = [book['title'] for book in results]
assert titles == sorted(titles)  # A-Z order
```

---

##### 11. test_order_by_year_descending()

**Purpose**: Verify ordering by year (newest first) works

**Endpoint**: `GET /api/books/?ordering=-publication_year`

**Test Steps:**
1. Create books with different years
2. Order by year (descending)
3. Verify results are newest to oldest

**Verification:**
```python
years = [book['publication_year'] for book in results]
assert years == sorted(years, reverse=True)  # Newest first
```

---

#### Permission Tests

##### 12. test_unauthenticated_read_access()

**Purpose**: Verify anyone can read books

**Endpoints:**
- `GET /api/books/`
- `GET /api/books/{id}/`

**Test Steps:**
1. Make GET requests without authentication
2. Verify both endpoints return 200 OK
3. Verify data is accessible

**Expected**: Read access allowed for everyone

---

##### 13. test_authenticated_create_access()

**Purpose**: Verify authenticated users can create

**Endpoint**: `POST /api/books/create/`

**Test Steps:**
1. Authenticate with valid token
2. Create book
3. Verify creation succeeds

**Expected**: 201 CREATED

---

##### 14. test_invalid_token_denied()

**Purpose**: Verify invalid tokens are rejected

**Endpoint**: `POST /api/books/create/`

**Test Steps:**
1. Use invalid token
2. Attempt to create book
3. Verify request is denied

**Expected**: 401 UNAUTHORIZED

---

#### Combined Features Tests

##### 15. test_filter_search_and_order()

**Purpose**: Verify all features work together

**Endpoint**: `GET /api/books/?author={id}&search={keyword}&ordering={field}`

**Test Steps:**
1. Apply filter, search, and ordering
2. Verify results match all criteria
3. Verify results are properly ordered

**Example:**
```bash
GET /api/books/?author=1&search=Harry&ordering=-publication_year
```

**Verification:**
- All books have author=1
- All titles contain "Harry"
- Results ordered by year (descending)

---

## Understanding Test Results

### Successful Test Run

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................
----------------------------------------------------------------------
Ran 37 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

**Explanation:**
- ✅ All 37 tests passed
- ✅ No errors or failures
- ✅ Test database created and destroyed automatically
- ✅ Each dot represents a passing test

---

### Failed Test Example

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..............F......................
======================================================================
FAIL: test_create_book_authenticated (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "api/test_views.py", line 145, in test_create_book_authenticated
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
AssertionError: 400 != 201

----------------------------------------------------------------------
Ran 37 tests in 2.567s

FAILED (failures=1)
```

**Explanation:**
- ❌ 1 test failed
- ❌ Expected 201 CREATED but got 400 BAD REQUEST
- ❌ Issue in book creation validation
- **Action**: Check the endpoint implementation

---

### Error in Test Example

```
ERROR: test_list_books (api.test_views.BookAPITestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "api/test_views.py", line 95, in test_list_books
    self.assertEqual(response.data['count'], 3)
KeyError: 'count'

----------------------------------------------------------------------
Ran 37 tests in 1.234s

FAILED (errors=1)
```

**Explanation:**
- ❌ 1 test error (not failure)
- ❌ Response doesn't have 'count' key
- ❌ Possible issue with pagination
- **Action**: Check pagination settings

---

## Test Coverage

### Measuring Coverage

Install coverage tool:
```bash
pip install coverage
```

Run tests with coverage:
```bash
coverage run --source='api' manage.py test api
coverage report
```

**Example Output:**
```
Name                      Stmts   Miss  Cover
---------------------------------------------
api/__init__.py               0      0   100%
api/models.py                20      0   100%
api/serializers.py           30      2    93%
api/views.py                 55      3    95%
api/test_views.py           450      0   100%
---------------------------------------------
TOTAL                       555      5    99%
```

Generate HTML coverage report:
```bash
coverage html
```

View report:
```bash
# Open htmlcov/index.html in browser
```

---

## Continuous Testing

### Test-Driven Development (TDD)

1. **Write test first** (fails)
2. **Write minimal code** to pass test
3. **Refactor** while keeping tests green

### Pre-Commit Testing

Create a pre-commit hook:

**`.git/hooks/pre-commit`**:
```bash
#!/bin/bash
python manage.py test api
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

### CI/CD Integration

**GitHub Actions Example** (`.github/workflows/test.yml`):
```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test api
```

---

## Best Practices

### ✅ DO

- Write tests for every new feature
- Keep tests independent and isolated
- Use descriptive test names
- Test edge cases and error conditions
- Run tests before committing code
- Maintain high test coverage (>90%)
- Document complex test scenarios

### ❌ DON'T

- Skip writing tests ("I'll add them later")
- Make tests dependent on each other
- Use production database for testing
- Ignore failing tests
- Test implementation details (test behavior)
- Leave commented-out test code

---

## Troubleshooting

### Common Issues

**Issue 1: Tests fail with database errors**

**Solution**: Ensure migrations are up to date
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py test api
```

---

**Issue 2: Token authentication doesn't work in tests**

**Solution**: Check token creation in setUp()
```python
self.token = Token.objects.create(user=self.user)
self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
```

---

**Issue 3: Tests pass locally but fail in CI**

**Solution**: Check for:
- Environment-specific settings
- Database differences
- Missing dependencies
- Timezone issues

---

## Summary

### Test Suite Overview

| Test Class | Tests | Coverage |
|------------|-------|----------|
| BookAPITestCase | 11 | CRUD operations |
| BookFilteringTestCase | 5 | Filtering |
| BookSearchingTestCase | 5 | Searching |
| BookOrderingTestCase | 5 | Ordering |
| BookPermissionsTestCase | 8 | Auth & Permissions |
| BookCombinedFeaturesTestCase | 3 | Combined features |
| **TOTAL** | **37** | **Complete coverage** |

### Quick Reference

```bash
# Run all tests
python manage.py test api

# Run specific test class
python manage.py test api.test_views.BookAPITestCase

# Run with verbose output
python manage.py test api --verbosity=2

# Run with coverage
coverage run --source='api' manage.py test api
coverage report

# Keep test database
python manage.py test api --keepdb
```

### Key Takeaways

✅ **37 comprehensive tests** covering all functionality  
✅ **100% endpoint coverage** - every endpoint is tested  
✅ **Security testing** - authentication and permissions verified  
✅ **Feature testing** - filtering, searching, ordering validated  
✅ **Well-documented** - clear test names and docstrings  
✅ **Easy to run** - simple commands for all scenarios  
✅ **Maintainable** - organized into logical test classes  

The test suite ensures the Book API is robust, secure, and behaves correctly under all conditions!
