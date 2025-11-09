# CRUD Operations Documentation

This document demonstrates all CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django's shell.

## 1. Create Operation

```python
# Import the Book model
>>> from bookshelf.models import Book

# Create a new book instance
>>> book = Book(title="1984", author="George Orwell", publication_year=1949)
>>> book.save()

# Verify creation by checking the book's id
>>> print(book.id)
1
```

## 2. Read Operation

```python
# Retrieve the book by title
>>> book = Book.objects.get(title="1984")

# Display all attributes
>>> print(f"Title: {book.title}")
Title: 1984
>>> print(f"Author: {book.author}")
Author: George Orwell
>>> print(f"Publication Year: {book.publication_year}")
Publication Year: 1949
```

## 3. Update Operation

```python
# Get the book and update its title
>>> book = Book.objects.get(title="1984")
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

# Verify the update
>>> updated_book = Book.objects.get(title="Nineteen Eighty-Four")
>>> print(f"Updated title: {updated_book.title}")
Updated title: Nineteen Eighty-Four
```

## 4. Delete Operation

```python
# Get and delete the book
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
(1, {'bookshelf.Book': 1})

# Verify deletion
>>> Book.objects.all().count()
0
```