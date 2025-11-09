# Updating Book Information

To update a book's information in the database, use these commands in the Django shell:

```python
# Import the Book model
>>> from bookshelf.models import Book

# Retrieve the book we want to update
>>> book = Book.objects.get(title="1984")

# Update the title
>>> book.title = "Nineteen Eighty-Four"
>>> book.save()

# Verify the update
>>> updated_book = Book.objects.get(title="Nineteen Eighty-Four")
>>> print(f"Updated title: {updated_book.title}")
Updated title: Nineteen Eighty-Four
```