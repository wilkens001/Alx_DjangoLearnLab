# Complete CRUD Operations Documentation

## Initial Setup
First, we need to enter the Django shell:
```python
python manage.py shell
```

## Import the Model
```python
from bookshelf.models import Book
```

## Create Operation
```python
# Create a new book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
print(f"Created book: {book}")
# Expected output: Created book: 1984 by George Orwell (1949)
```

## Retrieve Operation
```python
# Retrieve the book we just created
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
# Expected output:
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```

## Update Operation
```python
# Retrieve the book and update its title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Verify the update
updated_book = Book.objects.get(id=book.id)
print(f"Updated title: {updated_book.title}")
# Expected output: Updated title: Nineteen Eighty-Four
```

## Delete Operation
```python
# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify the deletion by trying to get all books
all_books = Book.objects.all()
print(f"Number of books in database: {len(all_books)}")
# Expected output: Number of books in database: 0
```