"""
URL configuration for the bookshelf app.

This module defines URL patterns for book CRUD operations with
permission-based access control.
"""

from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    # Book list and search
    path('books/', views.book_list, name='book_list'),
    
    # Book detail
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    
    # Book create
    path('books/create/', views.book_create, name='book_create'),
    
    # Book edit
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    
    # Book delete
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Form example demonstrating CSRF protection
    path('form-example/', views.form_example, name='form_example'),
]
