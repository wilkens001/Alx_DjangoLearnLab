"""
Views for the bookshelf app with permission-based access control.

This module implements CRUD operations for books with Django's permission system.
Each view is protected by the appropriate permission decorator to ensure only
authorized users can perform specific actions.

Permissions used:
- bookshelf.can_view: Required to view book details
- bookshelf.can_create: Required to create new books
- bookshelf.can_edit: Required to edit existing books
- bookshelf.can_delete: Required to delete books
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Book
from django import forms


class BookForm(forms.ModelForm):
    """
    Form for creating and editing Book instances.
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter publication year'}),
        }


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to list all books with secure search functionality.
    
    Requires: bookshelf.can_view permission
    
    This view displays all books in the database with optional search filtering.
    Users without the can_view permission will receive a 403 Forbidden error.
    
    SECURITY MEASURES:
    1. SQL Injection Prevention: Uses Django ORM's parameterized queries
    2. XSS Prevention: All output is automatically escaped in templates
    3. Input Validation: Search query is validated and sanitized
    """
    # Get the search query from GET parameters
    # SECURITY: Using request.GET.get() safely retrieves user input
    search_query = request.GET.get('search', '').strip()
    
    # Start with all books
    books = Book.objects.all()
    
    if search_query:
        # SECURITY: SQL Injection Prevention
        # Using Django ORM's Q objects and filter() method ensures that
        # the search query is properly parameterized and escaped.
        # This prevents SQL injection attacks by never directly interpolating
        # user input into SQL queries.
        #
        # WRONG (vulnerable to SQL injection):
        # books = Book.objects.raw(f"SELECT * FROM book WHERE title LIKE '%{search_query}%'")
        #
        # CORRECT (safe from SQL injection):
        from django.db.models import Q
        
        # Validate search query length to prevent abuse
        if len(search_query) > 200:
            messages.warning(request, 'Search query too long. Please use fewer characters.')
            search_query = search_query[:200]
        
        # Use Q objects for complex queries with proper parameterization
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query)
        )
    
    # Order results for consistent display
    books = books.order_by('title')
    
    context = {
        'books': books,
        'title': 'Book List',
        'search_query': search_query  # Pass back for display in template
    }
    return render(request, 'bookshelf/book_list.html', context)


@permission_required('bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    View to display details of a specific book.
    
    Requires: bookshelf.can_view permission
    
    Args:
        pk: Primary key of the book to display
    """
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
        'title': f'Book Details: {book.title}'
    }
    return render(request, 'bookshelf/book_detail.html', context)


@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book.
    
    Requires: bookshelf.can_create permission
    
    This view handles both GET (display form) and POST (process form) requests.
    Only users with can_create permission can access this view.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('bookshelf:book_list')
    else:
        form = BookForm()
    
    context = {
        'form': form,
        'title': 'Create New Book',
        'action': 'Create'
    }
    return render(request, 'bookshelf/book_form.html', context)


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book.
    
    Requires: bookshelf.can_edit permission
    
    Args:
        pk: Primary key of the book to edit
    
    This view handles both GET (display form with current data) and POST
    (process form submission) requests. Only users with can_edit permission
    can access this view.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('bookshelf:book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    
    context = {
        'form': form,
        'book': book,
        'title': f'Edit Book: {book.title}',
        'action': 'Update'
    }
    return render(request, 'bookshelf/book_form.html', context)


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book.
    
    Requires: bookshelf.can_delete permission
    
    Args:
        pk: Primary key of the book to delete
    
    This view displays a confirmation page on GET requests and deletes the
    book on POST requests. Only users with can_delete permission can access
    this view.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('bookshelf:book_list')
    
    context = {
        'book': book,
        'title': f'Delete Book: {book.title}'
    }
    return render(request, 'bookshelf/book_confirm_delete.html', context)


def form_example(request):
    """
    Example view demonstrating CSRF protection and secure form handling.
    
    This view serves as an educational example showing Django's security features:
    1. CSRF token protection for form submissions
    2. Input validation and sanitization
    3. XSS prevention through output escaping
    
    SECURITY MEASURES:
    - CSRF middleware validates the token on POST requests
    - All user input is validated before processing
    - Output is automatically escaped in templates
    """
    if request.method == 'POST':
        # SECURITY: Input Validation
        # Always validate and sanitize user input before processing
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation (in production, use Django forms for robust validation)
        if name and email and message:
            # Process the form data securely
            # In a real application, you would save to database, send email, etc.
            messages.success(
                request, 
                f'Thank you, {name}! Your message has been received securely.'
            )
            return redirect('bookshelf:form_example')
        else:
            messages.error(request, 'All fields are required.')
    
    return render(request, 'bookshelf/form_example.html')
