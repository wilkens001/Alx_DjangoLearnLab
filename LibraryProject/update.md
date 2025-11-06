# Updating a Book Entry

To update a book entry, we'll use the following commands in the Django shell:

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
>>> updated_book = Book.objects.get(id=book.id)
>>> print(f"Updated title: {updated_book.title}")
Updated title: Nineteen Eighty-Four
```