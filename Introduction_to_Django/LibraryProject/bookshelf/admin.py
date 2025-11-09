from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model"""
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search capability for these fields
    search_fields = ['title', 'author']
    
    # Add filters in the right sidebar
    list_filter = ('publication_year', 'author')
    
    # Order entries by title by default
    ordering = ('title',)