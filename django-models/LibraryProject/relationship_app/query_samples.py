"""Sample queries demonstrating ForeignKey, ManyToMany, and OneToOne relationships."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name):
    """Query all books by a specific author name."""
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name):
    """List all books in a library by library name."""
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return lib.books.all()


def librarian_for_library(library_name):
    """Retrieve the librarian for a library by name."""
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return None
    # Because of OneToOneField with related_name='librarian' we can access directly
    return getattr(lib, 'librarian', None)


if __name__ == '__main__':
    # Example usage: adjust names to match your DB or create sample data first
    print('Books by author "Jane Doe":')
    for b in books_by_author('Jane Doe'):
        print('-', b)

    print('\nBooks in library "Central Library":')
    for b in books_in_library('Central Library'):
        print('-', b)

    print('\nLibrarian for "Central Library":')
    libman = librarian_for_library('Central Library')
    print(libman)
