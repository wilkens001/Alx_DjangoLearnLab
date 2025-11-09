# Create Operation in Django Shell

To create a new book instance, use these commands in the Django shell:

```python
# Import the Book model
>>> from bookshelf.models import Book

# Create a new book instance
>>> book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()

# Expected output:
# No output shown when save() is successful
# The book instance is created in the database

# Verify creation by checking the book's id
>>> print(book.id)  # Should print a number (e.g., 1) indicating the book was saved
```

>>> book.save()    publication_year=1949

>>> print(f"Book created: {book}"))

Book created: 1984 by George Orwell (1949)

```# Expected output:
# A new Book object will be created in the database
# The book variable will contain the newly created Book instance
```