from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

def register_view(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

def login_view(request):
    """View for user login"""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('relationship_app:list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

def logout_view(request):
    """View for user logout"""
    from django.contrib.auth import logout
    logout(request)
    return render(request, 'relationship_app/logout.html')