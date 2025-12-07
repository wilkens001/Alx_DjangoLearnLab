"""
API Serializers for the advanced-api-project.

This module contains custom serializers for the Author and Book models,
implementing nested serialization and custom validation logic.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    
    This serializer handles the serialization and deserialization of Book instances,
    including all fields of the Book model. It implements custom validation to ensure
    data integrity.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - title: The book's title
        - publication_year: The year the book was published
        - author: Foreign key reference to the Author (ID)
    
    Custom Validation:
        - validate_publication_year: Ensures the publication year is not in the future
    
    Meta:
        model: Book model
        fields: All fields from the Book model ('__all__')
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from entering invalid publication dates.
        
        Args:
            value (int): The publication year to validate
        
        Returns:
            int: The validated publication year
        
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model with nested Book serialization.
    
    This serializer handles the serialization of Author instances and includes
    a nested representation of all books written by the author. This demonstrates
    how to handle one-to-many relationships in Django REST Framework serializers.
    
    Fields:
        - id: Auto-generated primary key (read-only)
        - name: The author's name
        - books: Nested serialization of all books by this author (read-only)
    
    The 'books' field uses the BookSerializer to serialize the related books.
    This creates a nested JSON structure where each author object contains
    an array of their books with complete book information.
    
    Relationship Handling:
        The 'books' field is populated using the related_name='books' defined
        in the Book model's author ForeignKey. This allows the serializer to
        access all books for an author using author.books.all().
        
        The many=True parameter indicates that this is a one-to-many relationship,
        and the read_only=True parameter ensures books are only included in
        serialization (GET requests) but not expected during creation/updates
        (POST/PUT requests).
    
    Example JSON Output:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                {
                    "id": 2,
                    "title": "Harry Potter and the Chamber of Secrets",
                    "publication_year": 1998,
                    "author": 1
                }
            ]
        }
    
    Meta:
        model: Author model
        fields: All fields plus the nested books relationship
    """
    
    # Nested serializer for related books
    # many=True indicates this is a one-to-many relationship
    # read_only=True means this field is only for output, not input
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
