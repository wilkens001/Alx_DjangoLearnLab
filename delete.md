# Delete Operation in Django Shell

```python
# Retrieve and delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify the deletion by trying to get all books
all_books = Book.objects.all()
print(f"Number of books in database: {len(all_books)}")

# Expected output:
# Number of books in database: 0
```