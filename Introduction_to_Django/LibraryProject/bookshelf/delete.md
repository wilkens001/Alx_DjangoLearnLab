# Deleting a Book Entry

```python
# Import the Book model
>>> from bookshelf.models import Book

# Retrieve the book we want to delete
>>> book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
>>> book.delete()
(1, {'bookshelf.Book': 1})

# Verify the deletion by trying to retrieve all books
>>> Book.objects.all().count()
0

# Trying to retrieve the deleted book will raise an exception
>>> Book.objects.get(title="Nineteen Eighty-Four")
DoesNotExist: Book matching query does not exist.
```