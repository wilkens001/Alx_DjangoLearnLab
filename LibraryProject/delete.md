# Deleting a Book Entry

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
>>> Book.objects.all().count()
0
```