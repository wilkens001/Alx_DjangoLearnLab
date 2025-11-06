# Create Operation in Django Shell

```python
# Create a new book instance
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)

# Expected output:
# A new Book object will be created in the database
# The book variable will contain the newly created Book instance
```