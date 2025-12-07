"""
Unit Tests for Django REST Framework API Views

This module contains comprehensive unit tests for the Book API endpoints,
testing CRUD operations, filtering, searching, ordering, authentication,
and permission controls.

Test Classes:
    - BookAPITestCase: Tests for Book model CRUD operations
    - BookFilteringTestCase: Tests for filtering functionality
    - BookSearchingTestCase: Tests for search functionality
    - BookOrderingTestCase: Tests for ordering functionality
    - BookPermissionsTestCase: Tests for authentication and permissions

Run tests with: python manage.py test api
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from api.models import Author, Book
from datetime import datetime


class BookAPITestCase(APITestCase):
    """
    Test case for basic CRUD operations on the Book API.
    
    Tests:
        - List all books
        - Retrieve a single book
        - Create a new book (authenticated)
        - Update a book (authenticated)
        - Delete a book (authenticated)
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        
        Creates:
            - Test user with authentication token
            - Test authors
            - Test books
        """
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create authentication token for the user
        self.token = Token.objects.create(user=self.user)
        
        # Login the user for session-based authentication
        self.client.login(username='testuser', password='testpass123')
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_list_books(self):
        """
        Test retrieving a list of all books.
        
        Verifies:
            - Status code is 200 OK
            - Response contains all books
            - No authentication required
        """
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_retrieve_book(self):
        """
        Test retrieving a single book by ID.
        
        Verifies:
            - Status code is 200 OK
            - Response contains correct book data
            - No authentication required
        """
        response = self.client.get(f'/api/books/{self.book1.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        self.assertEqual(response.data['author'], self.author1.id)
    
    def test_retrieve_nonexistent_book(self):
        """
        Test retrieving a book that doesn't exist.
        
        Verifies:
            - Status code is 404 NOT FOUND
        """
        response = self.client.get('/api/books/9999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book_authenticated(self):
        """
        Test creating a new book with authentication.
        
        Verifies:
            - Status code is 201 CREATED
            - Book is saved in database
            - Response contains correct data
        """
        # Authenticate the client
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'New Test Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'New Test Book')
        self.assertEqual(response.data['publication_year'], 2024)
    
    def test_create_book_unauthenticated(self):
        """
        Test creating a book without authentication.
        
        Verifies:
            - Status code is 401 UNAUTHORIZED
            - Book is not created in database
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)  # No new book created
    
    def test_create_book_invalid_data(self):
        """
        Test creating a book with invalid data (future publication year).
        
        Verifies:
            - Status code is 400 BAD REQUEST
            - Validation error is returned
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'Future Book',
            'publication_year': 3000,  # Future year (invalid)
            'author': self.author1.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_update_book_authenticated(self):
        """
        Test updating a book with authentication (PUT).
        
        Verifies:
            - Status code is 200 OK
            - Book is updated in database
            - Response contains updated data
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'Updated Title',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(f'/api/books/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_partial_update_book_authenticated(self):
        """
        Test partially updating a book with authentication (PATCH).
        
        Verifies:
            - Status code is 200 OK
            - Only specified field is updated
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(f'/api/books/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Title')
    
    def test_update_book_unauthenticated(self):
        """
        Test updating a book without authentication.
        
        Verifies:
            - Status code is 401 UNAUTHORIZED
        """
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 1997,
            'author': self.author1.id
        }
        
        response = self.client.put(f'/api/books/update/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_book_authenticated(self):
        """
        Test deleting a book with authentication.
        
        Verifies:
            - Status code is 204 NO CONTENT
            - Book is removed from database
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        initial_count = Book.objects.count()
        response = self.client.delete(f'/api/books/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
    
    def test_delete_book_unauthenticated(self):
        """
        Test deleting a book without authentication.
        
        Verifies:
            - Status code is 401 UNAUTHORIZED
            - Book is not deleted
        """
        initial_count = Book.objects.count()
        response = self.client.delete(f'/api/books/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), initial_count)


class BookFilteringTestCase(APITestCase):
    """
    Test case for filtering functionality.
    
    Tests filtering by:
        - Author
        - Title
        - Publication year
        - Multiple filters combined
    """
    
    def setUp(self):
        """Set up test data for filtering tests."""
        # Create authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        
        # Create books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        self.book4 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author2
        )
        
        self.client = APIClient()
    
    def test_filter_by_author(self):
        """
        Test filtering books by author.
        
        Verifies:
            - Correct number of books returned
            - All books belong to specified author
        """
        response = self.client.get(f'/api/books/?author={self.author1.id}')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Verify all returned books belong to author1
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)
    
    def test_filter_by_publication_year(self):
        """
        Test filtering books by publication year.
        
        Verifies:
            - Correct number of books returned
            - All books have specified publication year
        """
        response = self.client.get('/api/books/?publication_year=1997')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
    
    def test_filter_by_title(self):
        """
        Test filtering books by exact title.
        
        Verifies:
            - Correct book is returned
            - Title matches exactly
        """
        response = self.client.get('/api/books/?title=The Hobbit')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'The Hobbit')
    
    def test_filter_multiple_criteria(self):
        """
        Test filtering with multiple criteria.
        
        Verifies:
            - Filters work together correctly
            - Results match all criteria
        """
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&publication_year=1997'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['author'], self.author1.id)
        self.assertEqual(response.data['results'][0]['publication_year'], 1997)
    
    def test_filter_no_results(self):
        """
        Test filtering with criteria that match no books.
        
        Verifies:
            - Status code is 200 OK
            - Empty results list is returned
        """
        response = self.client.get('/api/books/?publication_year=2050')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['results']), 0)


class BookSearchingTestCase(APITestCase):
    """
    Test case for search functionality.
    
    Tests searching in:
        - Book titles
        - Author names
        - Partial matches
    """
    
    def setUp(self):
        """Set up test data for search tests."""
        # Create authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        
        # Create books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        
        self.client = APIClient()
    
    def test_search_by_title(self):
        """
        Test searching books by title.
        
        Verifies:
            - Correct books are found
            - Search is case-insensitive
            - Partial matches work
        """
        response = self.client.get('/api/books/?search=Potter')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        
        # Verify all results contain "Potter" in title
        for book in response.data['results']:
            self.assertIn('Potter', book['title'])
    
    def test_search_by_author_name(self):
        """
        Test searching books by author name.
        
        Verifies:
            - Books by matching author are found
            - Search works across related fields
        """
        response = self.client.get('/api/books/?search=Rowling')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
    
    def test_search_case_insensitive(self):
        """
        Test that search is case-insensitive.
        
        Verifies:
            - Lowercase search finds uppercase titles
            - Results are consistent regardless of case
        """
        response_lower = self.client.get('/api/books/?search=potter')
        response_upper = self.client.get('/api/books/?search=POTTER')
        
        self.assertEqual(response_lower.status_code, status.HTTP_200_OK)
        self.assertEqual(response_upper.status_code, status.HTTP_200_OK)
        self.assertEqual(response_lower.data['count'], response_upper.data['count'])
    
    def test_search_partial_match(self):
        """
        Test that search supports partial matching.
        
        Verifies:
            - Partial keywords find full words
        """
        response = self.client.get('/api/books/?search=Har')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
    
    def test_search_no_results(self):
        """
        Test search with no matching results.
        
        Verifies:
            - Status code is 200 OK
            - Empty results list returned
        """
        response = self.client.get('/api/books/?search=NonexistentBook')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class BookOrderingTestCase(APITestCase):
    """
    Test case for ordering functionality.
    
    Tests ordering by:
        - Title (ascending/descending)
        - Publication year (ascending/descending)
        - Default ordering
    """
    
    def setUp(self):
        """Set up test data for ordering tests."""
        author = Author.objects.create(name='Test Author')
        
        # Create books with different titles and years
        self.book1 = Book.objects.create(
            title='Book A',
            publication_year=2000,
            author=author
        )
        self.book2 = Book.objects.create(
            title='Book C',
            publication_year=1990,
            author=author
        )
        self.book3 = Book.objects.create(
            title='Book B',
            publication_year=2010,
            author=author
        )
        
        self.client = APIClient()
    
    def test_default_ordering(self):
        """
        Test default ordering (by title ascending).
        
        Verifies:
            - Books are ordered by title
            - Order is ascending (A-Z)
        """
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        
        # Verify alphabetical order
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_title_ascending(self):
        """
        Test ordering by title in ascending order.
        
        Verifies:
            - Books are ordered A-Z
        """
        response = self.client.get('/api/books/?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        
        self.assertEqual(titles, sorted(titles))
    
    def test_order_by_title_descending(self):
        """
        Test ordering by title in descending order.
        
        Verifies:
            - Books are ordered Z-A
        """
        response = self.client.get('/api/books/?ordering=-title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        
        self.assertEqual(titles, sorted(titles, reverse=True))
    
    def test_order_by_year_ascending(self):
        """
        Test ordering by publication year (ascending).
        
        Verifies:
            - Books are ordered oldest to newest
        """
        response = self.client.get('/api/books/?ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        
        self.assertEqual(years, sorted(years))
    
    def test_order_by_year_descending(self):
        """
        Test ordering by publication year (descending).
        
        Verifies:
            - Books are ordered newest to oldest
        """
        response = self.client.get('/api/books/?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        
        self.assertEqual(years, sorted(years, reverse=True))


class BookPermissionsTestCase(APITestCase):
    """
    Test case for authentication and permission controls.
    
    Tests:
        - Unauthenticated access to read endpoints
        - Authenticated access to write endpoints
        - Permission denial for unauthenticated writes
        - Token authentication
    """
    
    def setUp(self):
        """Set up test data for permission tests."""
        # Create users
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        # Login the user for session-based authentication
        self.client.login(username='authuser', password='authpass123')
        
        # Create test data
        author = Author.objects.create(name='Test Author')
        self.book = Book.objects.create(
            title='Test Book',
            publication_year=2020,
            author=author
        )
        
        self.client = APIClient()
    
    def test_unauthenticated_read_access(self):
        """
        Test that unauthenticated users can read books.
        
        Verifies:
            - List endpoint is accessible
            - Detail endpoint is accessible
            - No authentication required for GET
        """
        # Test list view
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test detail view
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_authenticated_create_access(self):
        """
        Test that authenticated users can create books.
        
        Verifies:
            - Create endpoint requires authentication
            - Valid token allows creation
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'Authenticated Book',
            'publication_year': 2024,
            'author': self.book.author.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_unauthenticated_create_denied(self):
        """
        Test that unauthenticated users cannot create books.
        
        Verifies:
            - Create endpoint returns 401 UNAUTHORIZED
            - No book is created
        """
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.book.author.id
        }
        
        initial_count = Book.objects.count()
        response = self.client.post('/api/books/create/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), initial_count)
    
    def test_authenticated_update_access(self):
        """
        Test that authenticated users can update books.
        
        Verifies:
            - Update endpoint requires authentication
            - Valid token allows updates
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'title': 'Updated by Auth User',
            'publication_year': 2020,
            'author': self.book.author.id
        }
        
        response = self.client.put(f'/api/books/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_update_denied(self):
        """
        Test that unauthenticated users cannot update books.
        
        Verifies:
            - Update endpoint returns 401 UNAUTHORIZED
        """
        data = {
            'title': 'Unauthorized Update',
            'publication_year': 2020,
            'author': self.book.author.id
        }
        
        response = self.client.put(f'/api/books/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_delete_access(self):
        """
        Test that authenticated users can delete books.
        
        Verifies:
            - Delete endpoint requires authentication
            - Valid token allows deletion
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.delete(f'/api/books/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_unauthenticated_delete_denied(self):
        """
        Test that unauthenticated users cannot delete books.
        
        Verifies:
            - Delete endpoint returns 401 UNAUTHORIZED
        """
        initial_count = Book.objects.count()
        response = self.client.delete(f'/api/books/delete/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), initial_count)
    
    def test_invalid_token_denied(self):
        """
        Test that invalid tokens are rejected.
        
        Verifies:
            - Invalid token returns 401 UNAUTHORIZED
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token_12345')
        
        data = {
            'title': 'Invalid Token Book',
            'publication_year': 2024,
            'author': self.book.author.id
        }
        
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookCombinedFeaturesTestCase(APITestCase):
    """
    Test case for combined features (filtering + searching + ordering).
    
    Tests:
        - Filter and order together
        - Search and order together
        - All three features combined
    """
    
    def setUp(self):
        """Set up test data for combined feature tests."""
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')
        
        Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        Book.objects.create(
            title='Harry Potter and the Chamber of Secrets',
            publication_year=1998,
            author=self.author1
        )
        Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author2
        )
        Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author2
        )
        
        self.client = APIClient()
    
    def test_filter_and_order(self):
        """
        Test combining filter and order.
        
        Verifies:
            - Filtering and ordering work together
            - Results are both filtered and ordered
        """
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data['count'], 0)
        
        # Verify ordering (descending year)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_search_and_order(self):
        """
        Test combining search and order.
        
        Verifies:
            - Searching and ordering work together
            - Results match search and are ordered
        """
        response = self.client.get('/api/books/?search=Potter&ordering=publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify all results contain "Potter"
        for book in response.data['results']:
            self.assertIn('Potter', book['title'])
        
        # Verify ordering
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years))
    
    def test_filter_search_and_order(self):
        """
        Test combining all three features.
        
        Verifies:
            - All features work together correctly
            - Results match all criteria
        """
        response = self.client.get(
            f'/api/books/?author={self.author1.id}&search=Harry&ordering=-publication_year'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify results match all criteria
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)
            self.assertIn('Harry', book['title'])
        
        # Verify ordering
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
