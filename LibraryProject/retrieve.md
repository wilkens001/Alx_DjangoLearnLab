# Retrieving a Book Entry

To retrieve a book entry, we'll use the following commands in the Django shell:

```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> print(f"Title: {book.title}")
Title: 1984
>>> print(f"Author: {book.author}")
Author: George Orwell
>>> print(f"Publication Year: {book.publication_year}")
Publication Year: 1949
```