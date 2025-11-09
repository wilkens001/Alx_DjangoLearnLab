# Retrieving Book Information

To retrieve a book instance from the database, use these commands in the Django shell:

```python
# Import the Book model
>>> from bookshelf.models import Book

# Retrieve the book by title
>>> book = Book.objects.get(title="1984")

# Display all attributes of the book
>>> print(f"Title: {book.title}")
Title: 1984
>>> print(f"Author: {book.author}")
Author: George Orwell
>>> print(f"Publication Year: {book.publication_year}")
Publication Year: 1949

# Alternative: use the string representation
>>> print(book)
1984 by George Orwell (1949)
```