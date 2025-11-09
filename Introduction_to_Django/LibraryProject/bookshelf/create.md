# Create Operation in Django Shell

```python
# Import the Book model
>>> from bookshelf.models import Book

# Create a new book instance using objects.create()
>>> book = Book.objects.create(
...     title="1984",
...     author="George Orwell",
...     publication_year=1949
... )

# Expected output:
# <Book: 1984 by George Orwell (1949)>

# Verify creation by checking the book's id
>>> print(book.id)  # Should print a number (e.g., 1) indicating the book was saved
1
```