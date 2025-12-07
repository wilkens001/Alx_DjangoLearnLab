from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author model represents a book author.
    
    This model stores basic information about authors who write books.
    It has a one-to-many relationship with the Book model, meaning
    one author can write multiple books.
    
    Fields:
        name (CharField): The full name of the author (max 100 characters)
    
    Methods:
        __str__: Returns the author's name for string representation
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """Return the author's name as string representation."""
        return self.name


class Book(models.Model):
    """
    Book model represents a published book.
    
    This model stores information about books and their relationship with authors.
    Each book is linked to one author through a foreign key relationship.
    
    Fields:
        title (CharField): The title of the book (max 200 characters)
        publication_year (IntegerField): The year the book was published
        author (ForeignKey): Foreign key reference to the Author model,
                            establishing a one-to-many relationship where
                            one author can have multiple books. When an author
                            is deleted, all their books are also deleted (CASCADE).
    
    Methods:
        __str__: Returns the book's title for string representation
    
    Related name:
        'books' - Allows reverse lookup from Author to all their books
        Example: author.books.all() returns all books by that author
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    
    def __str__(self):
        """Return the book's title as string representation."""
        return self.title
