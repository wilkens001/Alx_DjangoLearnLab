from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Blog Post model representing a blog post in the system.
    
    Fields:
        title: The title of the blog post (max 200 characters)
        content: The main content of the blog post
        published_date: The date and time when the post was published
        author: The user who authored the post
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title
