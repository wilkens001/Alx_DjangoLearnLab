from django.shortcuts import render
from .models import Post


def home(request):
    """Display the home page with recent blog posts."""
    posts = Post.objects.all().order_by('-published_date')[:5]
    return render(request, 'blog/home.html', {'posts': posts})
