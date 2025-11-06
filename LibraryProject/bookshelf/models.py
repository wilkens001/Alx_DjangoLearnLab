from django.db import models

class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=200, help_text="Enter the title of the book")
    author = models.CharField(max_length=100, help_text="Enter the author of the book")
    publication_year = models.IntegerField(help_text="Enter the year the book was published")

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String representation of the Book model"""
        return f"{self.title} by {self.author} ({self.publication_year})"

    def get_absolute_url(self):
        """Returns the URL to access a particular book instance."""
        return f"/book/{self.id}"