from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm, PostForm


def home(request):
    """Display the home page with recent blog posts."""
    posts = Post.objects.all().order_by('-published_date')[:5]
    return render(request, 'blog/home.html', {'posts': posts})


def register(request):
    """
    Handle user registration.
    
    GET: Display the registration form.
    POST: Process the registration form and create a new user.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! You can now log in.')
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    """
    Handle user login.
    
    GET: Display the login form.
    POST: Authenticate user and log them in.
    """
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_page = request.GET.get('next', 'profile')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'blog/login.html')


def user_logout(request):
    """
    Handle user logout.
    Logs out the user and redirects to home page.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile(request):
    """
    Display and handle user profile management.
    
    GET: Display the user's profile with edit form.
    POST: Update the user's profile information.
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'blog/profile.html', context)


# ============================================================================
# Blog Post CRUD Views (Class-Based Views)
# ============================================================================

class PostListView(ListView):
    """
    Display a list of all blog posts.
    
    Accessible to all users (authenticated or not).
    Posts are ordered by publication date (newest first).
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Blog Posts'
        return context


class PostDetailView(DetailView):
    """
    Display a single blog post in detail.
    
    Accessible to all users (authenticated or not).
    Shows full content, author, and publication date.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to create new blog posts.
    
    The logged-in user is automatically set as the author.
    Redirects to the post detail page after successful creation.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Set the author to the current logged-in user before saving."""
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        context['button_text'] = 'Create Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Allow post authors to edit their own blog posts.
    
    Only the author of the post can access this view.
    Uses UserPassesTestMixin to ensure authorization.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        """Validate and save the updated post."""
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        Returns True if user is the author, False otherwise.
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        context['button_text'] = 'Update Post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Allow post authors to delete their own blog posts.
    
    Only the author of the post can access this view.
    Requires confirmation before deletion.
    Redirects to post list after successful deletion.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
    def test_func(self):
        """
        Check if the current user is the author of the post.
        Returns True if user is the author, False otherwise.
        """
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        """Override delete to add a success message."""
        messages.success(request, 'Your post has been deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context
