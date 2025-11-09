"""Sample queries demonstrating ForeignKey, ManyToMany, and OneToOne relationships."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def books_by_author(author_name):
    """Query all books by a specific author name.
    
    Args:
        author_name: Either an Author instance or the name of the author as string
        
    Returns:
        QuerySet of books by the specified author
    """
    if isinstance(author_name, Author):
        return Book.objects.filter(author=author_name)
    # Try to find the author first to avoid potential multiple DB hits
    try:
        author = Author.objects.get(name=author_name)
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        # Return empty queryset if author not found
        return Book.objects.none()


def books_in_library(library_name):
    """List all books in a library by library name."""
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        return []
    return lib.books.all()


def librarian_for_library(library):
    """Retrieve the librarian for a library.
    
    Args:
        library: Either a Library instance or the name of the library as string
        
    Returns:
        Librarian instance if found, None otherwise
    """
    # If a Library instance is passed
    if isinstance(library, Library):
        return Librarian.objects.filter(library=library).first()
    
    # If library name is passed as string
    try:
        # First try to get the library
        lib = Library.objects.get(name=library)
        # Then get its librarian
        return Librarian.objects.filter(library=lib).first()
    except Library.DoesNotExist:
        return None


if __name__ == '__main__':
    # Example usage: adjust names to match your DB or create sample data first
    
    # Query books by author name
    print('Books by author name "Jane Doe":')
    for book in books_by_author('Jane Doe'):
        print('-', book)
    
    # Query books by author object
    try:
        author = Author.objects.get(name='Jane Doe')
        print('\nBooks by author object:')
        for book in books_by_author(author):
            print('-', book)
    except Author.DoesNotExist:
        print('\nAuthor not found')

    # Query books in library
    print('\nBooks in library "Central Library":')
    for book in books_in_library('Central Library'):
        print('-', book)

    # Query librarian by library name
    print('\nLibrarian for library name "Central Library":')
    libman = librarian_for_library('Central Library')
    print('-', libman)
    
    # Query librarian by library object
    try:
        library = Library.objects.get(name='Central Library')
        print('\nLibrarian for library object:')
        libman = librarian_for_library(library)
        print('-', libman)
    except Library.DoesNotExist:
        print('\nLibrary not found')
