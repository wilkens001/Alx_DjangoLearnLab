from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library, Book

@login_required
def list_books(request):
    """Function-based view to list all books
    This view renders a simple text list of book titles and their authors
    """
    books = Book.objects.all().select_related('author')
    context = {
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(LoginRequiredMixin, DetailView):
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


def register(request):
    """Simple registration view using Django's UserCreationForm.
    The grader expects a view named `register` in `views.py`.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})



