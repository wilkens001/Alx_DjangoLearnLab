"""
Test script to verify the functionality of models and serializers.

This script demonstrates:
1. Creating Author and Book instances
2. Serializing data with custom serializers
3. Testing validation logic
4. Verifying nested serialization
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'advanced_api_project.settings')
django.setup()

from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import datetime

def test_models_and_serializers():
    """Test creating and serializing Author and Book instances."""
    
    print("=" * 80)
    print("TESTING MODELS AND SERIALIZERS")
    print("=" * 80)
    
    # Clean up existing data for testing
    Book.objects.all().delete()
    Author.objects.all().delete()
    
    # Test 1: Create Authors
    print("\n1. Creating Authors...")
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    print(f"   Created: {author1}")
    print(f"   Created: {author2}")
    
    # Test 2: Create Books
    print("\n2. Creating Books...")
    book1 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        publication_year=1997,
        author=author1
    )
    book2 = Book.objects.create(
        title="Harry Potter and the Chamber of Secrets",
        publication_year=1998,
        author=author1
    )
    book3 = Book.objects.create(
        title="A Game of Thrones",
        publication_year=1996,
        author=author2
    )
    print(f"   Created: {book1} by {book1.author}")
    print(f"   Created: {book2} by {book2.author}")
    print(f"   Created: {book3} by {book3.author}")
    
    # Test 3: Serialize a single Book
    print("\n3. Testing BookSerializer...")
    book_serializer = BookSerializer(book1)
    print(f"   Serialized Book: {book_serializer.data}")
    
    # Test 4: Serialize Author with nested Books
    print("\n4. Testing AuthorSerializer with nested books...")
    author_serializer = AuthorSerializer(author1)
    print(f"   Serialized Author with books:")
    print(f"   {author_serializer.data}")
    
    # Test 5: Test validation - valid year
    print("\n5. Testing BookSerializer validation (valid year)...")
    valid_data = {
        'title': 'Test Book',
        'publication_year': 2020,
        'author': author1.id
    }
    serializer = BookSerializer(data=valid_data)
    if serializer.is_valid():
        print(f"   ✓ Validation passed for year {valid_data['publication_year']}")
    else:
        print(f"   ✗ Validation failed: {serializer.errors}")
    
    # Test 6: Test validation - future year (should fail)
    print("\n6. Testing BookSerializer validation (future year)...")
    future_year = datetime.now().year + 1
    invalid_data = {
        'title': 'Future Book',
        'publication_year': future_year,
        'author': author1.id
    }
    serializer = BookSerializer(data=invalid_data)
    if serializer.is_valid():
        print(f"   ✗ Validation should have failed for future year {future_year}")
    else:
        print(f"   ✓ Validation correctly failed: {serializer.errors['publication_year'][0]}")
    
    # Test 7: Test reverse relationship
    print("\n7. Testing reverse relationship (author.books.all())...")
    print(f"   Books by {author1.name}:")
    for book in author1.books.all():
        print(f"      - {book.title} ({book.publication_year})")
    
    # Test 8: Serialize multiple Authors
    print("\n8. Testing serialization of multiple authors...")
    all_authors = Author.objects.all()
    authors_serializer = AuthorSerializer(all_authors, many=True)
    print(f"   Serialized {len(authors_serializer.data)} authors")
    for author_data in authors_serializer.data:
        print(f"      - {author_data['name']}: {len(author_data['books'])} book(s)")
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == '__main__':
    test_models_and_serializers()
