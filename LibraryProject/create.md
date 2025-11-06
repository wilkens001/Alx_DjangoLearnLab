# Creating a Book Entry# Creating a Book Entry# Create Operation in Django Shell



```python

>>> from bookshelf.models import Book

>>> book = Book(title="1984", author="George Orwell", publication_year=1949)To create a new book entry, we'll use the following commands in the Django shell:```python

>>> book.save()

```# Create a new book instance

```pythonbook = Book.objects.create(

>>> from bookshelf.models import Book    title="1984",

>>> book = Book(title="1984", author="George Orwell", publication_year=1949)    author="George Orwell",

>>> book.save()    publication_year=1949

>>> print(f"Book created: {book}"))

Book created: 1984 by George Orwell (1949)

```# Expected output:
# A new Book object will be created in the database
# The book variable will contain the newly created Book instance
```