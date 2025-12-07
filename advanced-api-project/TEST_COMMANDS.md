# Quick Test Commands Reference

## Run All Tests
```bash
python manage.py test api
```

## Run Specific Test Classes

### CRUD Operations Tests
```bash
python manage.py test api.test_views.BookAPITestCase
```

### Filtering Tests
```bash
python manage.py test api.test_views.BookFilteringTestCase
```

### Searching Tests
```bash
python manage.py test api.test_views.BookSearchingTestCase
```

### Ordering Tests
```bash
python manage.py test api.test_views.BookOrderingTestCase
```

### Permissions Tests
```bash
python manage.py test api.test_views.BookPermissionsTestCase
```

### Combined Features Tests
```bash
python manage.py test api.test_views.BookCombinedFeaturesTestCase
```

## Run Individual Tests

```bash
# Test creating a book (authenticated)
python manage.py test api.test_views.BookAPITestCase.test_create_book_authenticated

# Test filtering by author
python manage.py test api.test_views.BookFilteringTestCase.test_filter_by_author

# Test search functionality
python manage.py test api.test_views.BookSearchingTestCase.test_search_by_title

# Test ordering
python manage.py test api.test_views.BookOrderingTestCase.test_order_by_year_descending

# Test permissions
python manage.py test api.test_views.BookPermissionsTestCase.test_unauthenticated_create_denied
```

## Verbose Output
```bash
# Show test names as they run
python manage.py test api --verbosity=2

# Show all details
python manage.py test api --verbosity=3
```

## Other Useful Options
```bash
# Keep test database for inspection
python manage.py test api --keepdb

# Run tests in parallel (faster)
python manage.py test api --parallel

# Stop at first failure
python manage.py test api --failfast
```

## Test Coverage
```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run --source='api' manage.py test api

# Show report
coverage report

# Generate HTML report
coverage html
# Then open htmlcov/index.html
```

## Expected Output (All Passing)
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....................................
----------------------------------------------------------------------
Ran 37 tests in 2.345s

OK
Destroying test database for alias 'default'...
```

## Test Summary

| Category | Tests | Description |
|----------|-------|-------------|
| CRUD | 11 | Create, Read, Update, Delete operations |
| Filtering | 5 | Filter by author, title, year |
| Searching | 5 | Search in title and author name |
| Ordering | 5 | Order by title and year |
| Permissions | 8 | Authentication and access control |
| Combined | 3 | Multiple features together |
| **TOTAL** | **37** | **Complete test coverage** |

## For Full Documentation

See [TESTING_DOCUMENTATION.md](TESTING_DOCUMENTATION.md) for:
- Detailed test case descriptions
- Testing strategy
- Troubleshooting guide
- Best practices
- CI/CD integration
