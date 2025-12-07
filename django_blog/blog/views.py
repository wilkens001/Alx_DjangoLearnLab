from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Post
from .forms import CustomUserCreationForm, UserUpdateForm


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
