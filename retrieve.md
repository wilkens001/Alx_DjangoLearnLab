# Retrieve Operation in Django Shell

```python
# Retrieve the book we just created
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")

# Expected output:
# Title: 1984
# Author: George Orwell
# Publication Year: 1949
```