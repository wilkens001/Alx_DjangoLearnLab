# CRUD Operations Documentation

This document demonstrates all Create, Read, Update, and Delete (CRUD) operations for the Book model.

## Create Operation
```python
>>> from bookshelf.models import Book
>>> book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()
```

## Read Operation
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> print(book.title)
1984
>>> print(book.author)
George Orwell
>>> print(book.publication_year)
1949
```

## Update Operation
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()
```

## Delete Operation
```python
>>> from bookshelf.models import Book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
>>> Book.objects.all().count()
0
```