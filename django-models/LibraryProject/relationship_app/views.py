from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import ListView
# Import Library model first to ensure it's available for the class-based view
from .models import Library, Book

def list_books(request):
    """Function-based view to list all books
    This view renders a simple text list of book titles and their authors
    """
    books = Book.objects.all().select_related('author')
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """Class-based view to display details for a specific library.
    This view displays details of a specific library, listing all books available in that library.
    """
    model = Library  # Specify the Library model for the DetailView
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        """Optimize query by prefetching related books and their authors"""
        return Library.objects.prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        """Add additional context data"""
        context = super().get_context_data(**kwargs)
        # Ensure books are prefetched for the template
        context['library'] = self.get_object()
        return context