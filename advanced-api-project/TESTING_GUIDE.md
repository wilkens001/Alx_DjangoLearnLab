# Testing Guide for Advanced API Project

This guide provides step-by-step instructions for testing the API endpoints using various tools.

## Prerequisites

1. **Start the development server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

2. **Create a superuser** (for authentication testing):
   ```bash
   python manage.py createsuperuser
   ```

3. **Create an authentication token** (run in Django shell):
   ```bash
   python manage.py shell
   ```
   
   Then execute:
   ```python
   from django.contrib.auth.models import User
   from rest_framework.authtoken.models import Token
   
   # Get your user
   user = User.objects.get(username='your_username')
   
   # Create or get token
   token, created = Token.objects.get_or_create(user=user)
   print(f"Your token: {token.key}")
   ```

---

## Testing with curl (Command Line)

### 1. List All Books (No Authentication Required)

```bash
curl -X GET http://127.0.0.1:8000/api/books/
```

**Expected Response** (200 OK):
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Book Title",
            "publication_year": 2024,
            "author": 1
        }
    ]
}
```

### 2. Get Single Book (No Authentication Required)

```bash
curl -X GET http://127.0.0.1:8000/api/books/1/
```

**Expected Response** (200 OK):
```json
{
    "id": 1,
    "title": "Book Title",
    "publication_year": 2024,
    "author": 1
}
```

### 3. Search Books

```bash
# Search by title
curl -X GET "http://127.0.0.1:8000/api/books/?search=Potter"

# Order by publication year
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=publication_year"

# Descending order
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-publication_year"
```

### 4. Create a Book (Authentication Required)

**Replace `YOUR_TOKEN_HERE` with your actual token**:

```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Book\", \"publication_year\": 2024, \"author\": 1}"
```

**Expected Response** (201 Created):
```json
{
    "id": 2,
    "title": "Test Book",
    "publication_year": 2024,
    "author": 1
}
```

**Without Authentication** (401 Unauthorized):
```bash
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Test Book\", \"publication_year\": 2024, \"author\": 1}"
```

### 5. Update a Book (Authentication Required)

**Full Update (PUT)**:
```bash
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Updated Title\", \"publication_year\": 2024, \"author\": 1}"
```

**Partial Update (PATCH)**:
```bash
curl -X PATCH http://127.0.0.1:8000/api/books/1/update/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"New Title\"}"
```

**Expected Response** (200 OK):
```json
{
    "id": 1,
    "title": "New Title",
    "publication_year": 2024,
    "author": 1
}
```

### 6. Delete a Book (Authentication Required)

```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

**Expected Response** (204 No Content):
```
(No content)
```

### 7. Test Validation (Create with Invalid Data)

```bash
# Future publication year (should fail)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Future Book\", \"publication_year\": 3000, \"author\": 1}"
```

**Expected Response** (400 Bad Request):
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2024."
    ]
}
```

---

## Testing with Postman

### Setup

1. **Install Postman** from https://www.postman.com/downloads/
2. **Create a new Collection** called "Advanced API Tests"
3. **Set up Environment Variables**:
   - Variable: `base_url` = `http://127.0.0.1:8000`
   - Variable: `auth_token` = `YOUR_TOKEN_HERE`

### Request 1: List All Books

- **Method**: GET
- **URL**: `{{base_url}}/api/books/`
- **Headers**: None required
- **Body**: None
- **Expected Status**: 200 OK

### Request 2: Get Single Book

- **Method**: GET
- **URL**: `{{base_url}}/api/books/1/`
- **Headers**: None required
- **Body**: None
- **Expected Status**: 200 OK

### Request 3: Create Book

- **Method**: POST
- **URL**: `{{base_url}}/api/books/create/`
- **Headers**:
  - Key: `Authorization`, Value: `Token {{auth_token}}`
  - Key: `Content-Type`, Value: `application/json`
- **Body** (raw JSON):
  ```json
  {
      "title": "Postman Test Book",
      "publication_year": 2024,
      "author": 1
  }
  ```
- **Expected Status**: 201 Created

### Request 4: Update Book (PUT)

- **Method**: PUT
- **URL**: `{{base_url}}/api/books/1/update/`
- **Headers**:
  - Key: `Authorization`, Value: `Token {{auth_token}}`
  - Key: `Content-Type`, Value: `application/json`
- **Body** (raw JSON):
  ```json
  {
      "title": "Updated via Postman",
      "publication_year": 2024,
      "author": 1
  }
  ```
- **Expected Status**: 200 OK

### Request 5: Update Book (PATCH)

- **Method**: PATCH
- **URL**: `{{base_url}}/api/books/1/update/`
- **Headers**:
  - Key: `Authorization`, Value: `Token {{auth_token}}`
  - Key: `Content-Type`, Value: `application/json`
- **Body** (raw JSON):
  ```json
  {
      "title": "Partially Updated Title"
  }
  ```
- **Expected Status**: 200 OK

### Request 6: Delete Book

- **Method**: DELETE
- **URL**: `{{base_url}}/api/books/1/delete/`
- **Headers**:
  - Key: `Authorization`, Value: `Token {{auth_token}}`
- **Body**: None
- **Expected Status**: 204 No Content

---

## Testing with Python Requests Library

Create a test script `test_api.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = "YOUR_TOKEN_HERE"  # Replace with your actual token

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Test 1: List all books
print("\n=== Test 1: List All Books ===")
response = requests.get(f"{BASE_URL}/books/")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 2: Get single book
print("\n=== Test 2: Get Single Book ===")
response = requests.get(f"{BASE_URL}/books/1/")
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Create a book (requires auth)
print("\n=== Test 3: Create Book ===")
data = {
    "title": "Python Test Book",
    "publication_year": 2024,
    "author": 1
}
response = requests.post(f"{BASE_URL}/books/create/", json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 4: Update book (requires auth)
print("\n=== Test 4: Update Book ===")
book_id = response.json()['id']  # Use the ID from created book
data = {
    "title": "Updated Python Test Book",
    "publication_year": 2024,
    "author": 1
}
response = requests.put(f"{BASE_URL}/books/{book_id}/update/", json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 5: Delete book (requires auth)
print("\n=== Test 5: Delete Book ===")
response = requests.delete(f"{BASE_URL}/books/{book_id}/delete/", headers=headers)
print(f"Status: {response.status_code}")

# Test 6: Test validation (future year)
print("\n=== Test 6: Test Validation ===")
data = {
    "title": "Future Book",
    "publication_year": 3000,
    "author": 1
}
response = requests.post(f"{BASE_URL}/books/create/", json=data, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 7: Test unauthorized access
print("\n=== Test 7: Test Unauthorized Access ===")
data = {
    "title": "Unauthorized Book",
    "publication_year": 2024,
    "author": 1
}
response = requests.post(f"{BASE_URL}/books/create/", json=data)  # No headers
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
```

Run the script:
```bash
python test_api.py
```

---

## Testing with Django REST Framework's Browsable API

1. **Start the server**:
   ```bash
   python manage.py runserver
   ```

2. **Open in browser**:
   - List: http://127.0.0.1:8000/api/books/
   - Detail: http://127.0.0.1:8000/api/books/1/
   - Create: http://127.0.0.1:8000/api/books/create/

3. **Login** (top right corner):
   - Click "Log in"
   - Enter your superuser credentials

4. **Test operations**:
   - **GET**: Just navigate to the URL
   - **POST**: Fill in the HTML form at the bottom and click "POST"
   - **PUT/PATCH**: Navigate to detail URL, fill form, click "PUT" or "PATCH"
   - **DELETE**: Navigate to delete URL, click "DELETE"

---

## Test Scenarios Checklist

### Public Access (No Authentication)
- [ ] List all books (GET /api/books/)
- [ ] Get single book (GET /api/books/1/)
- [ ] Search books (GET /api/books/?search=term)
- [ ] Order books (GET /api/books/?ordering=title)

### Authenticated Access
- [ ] Create book with valid data (POST /api/books/create/)
- [ ] Update book with PUT (PUT /api/books/1/update/)
- [ ] Update book with PATCH (PATCH /api/books/1/update/)
- [ ] Delete book (DELETE /api/books/1/delete/)

### Validation Testing
- [ ] Create book with future year (should fail with 400)
- [ ] Create book with missing fields (should fail with 400)
- [ ] Create book with invalid author ID (should fail with 400)
- [ ] Update book with invalid data (should fail with 400)

### Permission Testing
- [ ] Try to create without auth (should fail with 401)
- [ ] Try to update without auth (should fail with 401)
- [ ] Try to delete without auth (should fail with 401)

### Error Handling
- [ ] Get non-existent book (should return 404)
- [ ] Update non-existent book (should return 404)
- [ ] Delete non-existent book (should return 404)

---

## Expected HTTP Status Codes

| Operation | Success Code | Error Codes |
|-----------|-------------|-------------|
| GET (List) | 200 OK | 500 Internal Server Error |
| GET (Detail) | 200 OK | 404 Not Found, 500 |
| POST (Create) | 201 Created | 400 Bad Request, 401 Unauthorized, 500 |
| PUT (Update) | 200 OK | 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 |
| PATCH (Partial Update) | 200 OK | 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 |
| DELETE | 204 No Content | 401 Unauthorized, 404 Not Found, 500 |

---

## Common Issues and Solutions

### Issue 1: Token Not Working
**Error**: `{"detail": "Invalid token."}`

**Solutions**:
- Verify token exists: `Token.objects.filter(user__username='youruser')`
- Regenerate token:
  ```python
  token = Token.objects.get(user__username='youruser')
  token.delete()
  token = Token.objects.create(user=user)
  ```

### Issue 2: CSRF Token Error
**Error**: `{"detail": "CSRF Failed: CSRF token missing or incorrect."}`

**Solution**: Add CSRF exemption for API endpoints or use token authentication

### Issue 3: Author Does Not Exist
**Error**: `{"author": ["Invalid pk \"1\" - object does not exist."]}`

**Solution**: Create an author first:
```python
python manage.py shell
from api.models import Author
Author.objects.create(name="Test Author")
```

### Issue 4: Database Not Migrated
**Error**: `no such table: api_book`

**Solution**: Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Sample Test Data

Create sample data in Django shell:

```python
python manage.py shell
```

```python
from api.models import Author, Book

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="J.R.R. Tolkien")
author3 = Author.objects.create(name="George Orwell")

# Create books
Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author1
)
Book.objects.create(
    title="Harry Potter and the Chamber of Secrets",
    publication_year=1998,
    author=author1
)
Book.objects.create(
    title="The Hobbit",
    publication_year=1937,
    author=author2
)
Book.objects.create(
    title="The Lord of the Rings",
    publication_year=1954,
    author=author2
)
Book.objects.create(
    title="1984",
    publication_year=1949,
    author=author3
)

print("Sample data created successfully!")
```

---

## Automated Testing Script

Save this as `automated_tests.sh` (Linux/Mac) or `automated_tests.ps1` (Windows):

**PowerShell Version** (`automated_tests.ps1`):
```powershell
$BASE_URL = "http://127.0.0.1:8000/api"
$TOKEN = "YOUR_TOKEN_HERE"

Write-Host "`n=== Testing API Endpoints ===" -ForegroundColor Green

# Test 1: List books
Write-Host "`nTest 1: List All Books" -ForegroundColor Yellow
curl.exe -X GET "$BASE_URL/books/"

# Test 2: Get single book
Write-Host "`nTest 2: Get Single Book" -ForegroundColor Yellow
curl.exe -X GET "$BASE_URL/books/1/"

# Test 3: Create book
Write-Host "`nTest 3: Create Book" -ForegroundColor Yellow
curl.exe -X POST "$BASE_URL/books/create/" `
  -H "Authorization: Token $TOKEN" `
  -H "Content-Type: application/json" `
  -d '{\"title\": \"Test Book\", \"publication_year\": 2024, \"author\": 1}'

Write-Host "`n=== Tests Completed ===" -ForegroundColor Green
```

Run: `.\automated_tests.ps1`

---

## Next Steps

1. Run through all test scenarios
2. Verify responses match expected results
3. Test edge cases
4. Document any issues found
5. Consider adding automated unit tests

For more information, see `API_VIEWS_CONFIGURATION.md` and `README.md`.
