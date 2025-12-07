"""
API Views for the advanced-api-project.

This module contains generic views for handling CRUD operations on the Book model
using Django REST Framework's generic views. These views provide a standardized
approach to API development with built-in support for authentication, permissions,
and data validation.

Views:
    - BookListView: Retrieves all books (GET) - Read-only for unauthenticated users
    - BookDetailView: Retrieves a single book by ID (GET) - Read-only for unauthenticated users
    - BookCreateView: Creates a new book (POST) - Requires authentication
    - BookUpdateView: Updates an existing book (PUT/PATCH) - Requires authentication
    - BookDeleteView: Deletes a book (DELETE) - Requires authentication
"""

from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    This view handles GET requests to retrieve a list of all Book instances
    in the database. It provides read-only access to both authenticated and
    unauthenticated users.
    
    Endpoints:
        GET /books/ - Returns a list of all books
    
    Permissions:
        - Read access: Anyone (authenticated or unauthenticated)
    
    Filters:
        - Supports searching by title
        - Supports ordering by title and publication_year
    
    Returns:
        200 OK: List of book objects with all fields
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only for everyone
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']  # Search by title or author name
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    This view handles GET requests to retrieve a specific Book instance
    identified by its primary key (ID). It provides read-only access to
    both authenticated and unauthenticated users.
    
    Endpoints:
        GET /books/<int:pk>/ - Returns details of a specific book
    
    Permissions:
        - Read access: Anyone (authenticated or unauthenticated)
    
    URL Parameters:
        pk (int): The primary key of the book to retrieve
    
    Returns:
        200 OK: Book object with all fields
        404 Not Found: If book with given ID doesn't exist
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only for everyone


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    This view handles POST requests to create a new Book instance.
    Only authenticated users can create books. The view automatically
    handles form submission, data validation through the BookSerializer,
    and returns the created object.
    
    Endpoints:
        POST /books/create/ - Creates a new book
    
    Permissions:
        - Create access: Authenticated users only
    
    Request Body (JSON):
        {
            "title": "Book Title",
            "publication_year": 2024,
            "author": 1  // Author ID
        }
    
    Returns:
        201 Created: Newly created book object
        400 Bad Request: If validation fails (e.g., invalid publication_year)
        401 Unauthorized: If user is not authenticated
    
    Validation:
        - title: Required, max 200 characters
        - publication_year: Required, cannot be in the future
        - author: Required, must be a valid author ID
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create
    
    def perform_create(self, serializer):
        """
        Custom create logic.
        
        This method is called after validation is successful but before
        the instance is saved. It can be used to set additional fields
        or perform custom actions during creation.
        
        Args:
            serializer: The validated serializer instance
        """
        # Save the book instance
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    This view handles PUT and PATCH requests to update an existing Book instance.
    Only authenticated users can update books. PUT requires all fields while
    PATCH allows partial updates.
    
    Endpoints:
        PUT /books/<int:pk>/update/ - Full update of a book
        PATCH /books/<int:pk>/update/ - Partial update of a book
    
    Permissions:
        - Update access: Authenticated users only
    
    URL Parameters:
        pk (int): The primary key of the book to update
    
    Request Body (JSON for PUT):
        {
            "title": "Updated Book Title",
            "publication_year": 2024,
            "author": 1  // Author ID
        }
    
    Request Body (JSON for PATCH - any subset):
        {
            "title": "Updated Title"  // Only update title
        }
    
    Returns:
        200 OK: Updated book object
        400 Bad Request: If validation fails
        401 Unauthorized: If user is not authenticated
        404 Not Found: If book with given ID doesn't exist
    
    Validation:
        - Same validation rules as CreateView apply
        - All fields are optional for PATCH requests
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update
    
    def perform_update(self, serializer):
        """
        Custom update logic.
        
        This method is called after validation is successful but before
        the instance is updated. It can be used to modify fields or
        perform custom actions during updates.
        
        Args:
            serializer: The validated serializer instance
        """
        # Save the updated book instance
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    This view handles DELETE requests to remove a Book instance from the database.
    Only authenticated users can delete books. The deletion is permanent and
    cannot be undone.
    
    Endpoints:
        DELETE /books/<int:pk>/delete/ - Deletes a specific book
    
    Permissions:
        - Delete access: Authenticated users only
    
    URL Parameters:
        pk (int): The primary key of the book to delete
    
    Returns:
        204 No Content: If deletion is successful
        401 Unauthorized: If user is not authenticated
        404 Not Found: If book with given ID doesn't exist
    
    Note:
        This performs a hard delete. Consider implementing soft deletes
        for production applications where data recovery might be needed.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete
