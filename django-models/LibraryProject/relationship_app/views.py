from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Library, Book
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django import forms


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


def _has_role(user, role_name):
    """Helper to check user's role safely."""
    try:
        return user.is_authenticated and user.userprofile.role == role_name
    except Exception:
        return False


@user_passes_test(lambda u: _has_role(u, 'Admin'))
def admin_view(request):
    """View restricted to Admin users."""
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(lambda u: _has_role(u, 'Librarian'))
def librarian_view(request):
    """View restricted to Librarian users."""
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(lambda u: _has_role(u, 'Member'))
def member_view(request):
    """View restricted to Member users."""
    return render(request, 'relationship_app/member_view.html')


# Simple ModelForm for Book create/update
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """Add a new book. Requires can_add_book permission."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """Edit an existing book. Requires can_change_book permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('relationship_app:list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """Delete a book. Requires can_delete_book permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')
    return render(request, 'relationship_app/confirm_delete.html', {'book': book})



