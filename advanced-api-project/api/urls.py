"""
URL Configuration for the API app.

This module defines the URL patterns for all API endpoints related to the Book model.
Each endpoint corresponds to a specific view that handles CRUD operations.

URL Patterns:
    - /books/ - ListView: Retrieves all books (GET)
    - /books/<int:pk>/ - DetailView: Retrieves a single book by ID (GET)
    - /books/create/ - CreateView: Creates a new book (POST)
    - /books/<int:pk>/update/ - UpdateView: Updates an existing book (PUT/PATCH)
    - /books/<int:pk>/delete/ - DeleteView: Deletes a book (DELETE)

Authentication:
    - Read operations (ListView, DetailView): Open to all users
    - Write operations (Create, Update, Delete): Require authentication

Usage Examples:
    GET /books/ - Returns list of all books
    GET /books/1/ - Returns details of book with ID 1
    POST /books/create/ - Creates a new book (requires auth)
    PUT /books/1/update/ - Updates book with ID 1 (requires auth)
    PATCH /books/1/update/ - Partially updates book with ID 1 (requires auth)
    DELETE /books/1/delete/ - Deletes book with ID 1 (requires auth)
"""

from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

# App namespace for reverse URL lookups
app_name = 'api'

urlpatterns = [
    # List all books - GET request
    # Endpoint: /books/
    # Permission: AllowAny (read-only for all users)
    # Returns: List of all book objects
    path('books/', BookListView.as_view(), name='book-list'),
    
    # Retrieve a single book by ID - GET request
    # Endpoint: /books/<int:pk>/
    # Permission: AllowAny (read-only for all users)
    # Returns: Single book object or 404 if not found
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # Create a new book - POST request
    # Endpoint: /books/create/
    # Permission: IsAuthenticated (requires authentication)
    # Returns: Newly created book object with 201 status
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # Update an existing book - PUT/PATCH request
    # Endpoint: /books/<int:pk>/update/
    # Permission: IsAuthenticated (requires authentication)
    # Returns: Updated book object with 200 status
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # Delete a book - DELETE request
    # Endpoint: /books/<int:pk>/delete/
    # Permission: IsAuthenticated (requires authentication)
    # Returns: 204 No Content on successful deletion
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
