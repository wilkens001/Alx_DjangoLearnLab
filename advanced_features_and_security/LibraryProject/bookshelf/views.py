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
    View to list all books.
    
    Requires: bookshelf.can_view permission
    
    This view displays all books in the database. Users without the can_view
    permission will receive a 403 Forbidden error.
    """
    books = Book.objects.all().order_by('title')
    context = {
        'books': books,
        'title': 'Book List'
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
