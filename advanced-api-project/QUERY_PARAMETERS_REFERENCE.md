# Quick Reference: API Query Parameters

## Base URL
```
http://127.0.0.1:8000/api/books/
```

## Filtering

### Filter by Author
```bash
GET /api/books/?author=1
```

### Filter by Title
```bash
GET /api/books/?title=The Hobbit
```

### Filter by Publication Year
```bash
GET /api/books/?publication_year=1997
```

### Multiple Filters
```bash
GET /api/books/?author=1&publication_year=1997
```

---

## Searching

### Search in Title
```bash
GET /api/books/?search=Potter
```

### Search in Author Name
```bash
GET /api/books/?search=Rowling
```

### Search Multiple Words
```bash
GET /api/books/?search=Harry Potter
```

---

## Ordering

### Order by Title (A-Z)
```bash
GET /api/books/?ordering=title
```

### Order by Title (Z-A)
```bash
GET /api/books/?ordering=-title
```

### Order by Year (Oldest First)
```bash
GET /api/books/?ordering=publication_year
```

### Order by Year (Newest First)
```bash
GET /api/books/?ordering=-publication_year
```

---

## Combined Queries

### Filter + Order
```bash
GET /api/books/?author=1&ordering=-publication_year
```

### Search + Order
```bash
GET /api/books/?search=Potter&ordering=publication_year
```

### Filter + Search + Order
```bash
GET /api/books/?author=1&search=Harry&ordering=-publication_year
```

---

## Python Examples

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api/books/"

# Filtering
response = requests.get(BASE_URL, params={'author': 1})

# Searching
response = requests.get(BASE_URL, params={'search': 'Potter'})

# Ordering
response = requests.get(BASE_URL, params={'ordering': '-publication_year'})

# Combined
response = requests.get(BASE_URL, params={
    'author': 1,
    'search': 'Harry',
    'ordering': '-publication_year'
})
```

---

## Query Parameter Reference

| Parameter | Values | Description |
|-----------|--------|-------------|
| `author` | Integer (ID) | Filter by author |
| `title` | String | Exact title match |
| `publication_year` | Integer (Year) | Filter by year |
| `search` | String | Search in title/author |
| `ordering` | `title`, `-title`, `publication_year`, `-publication_year` | Sort results |

**Note**: Use `-` prefix for descending order (e.g., `-publication_year`)

---

## Full Documentation

For complete documentation, see:
- [FILTERING_SEARCHING_ORDERING.md](FILTERING_SEARCHING_ORDERING.md) - Detailed implementation guide
- [README.md](README.md) - Full project documentation
- [API_VIEWS_CONFIGURATION.md](API_VIEWS_CONFIGURATION.md) - View configuration details
