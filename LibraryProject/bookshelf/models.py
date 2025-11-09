from django.db import models

# Create your models here.
class Book(models.Model):
    """
    Model representing a book in the library.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        """String representation of the Book model"""
        return f"{self.title} by {self.author} ({self.publication_year})"

    class Meta:
        """Meta options for the Book model"""
        ordering = ['title', 'author']
