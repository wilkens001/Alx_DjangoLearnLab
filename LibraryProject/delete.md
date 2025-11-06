# Deleting a Book Entry

To delete a book entry, we'll use the following commands in the Django shell:

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})
>>> all_books = Book.objects.all()
>>> print(f"Number of books in database: {len(all_books)}")
Number of books in database: 0
```