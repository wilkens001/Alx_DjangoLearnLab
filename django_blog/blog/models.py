from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    """
    Tag model for categorizing blog posts.
    
    Fields:
        name: The name of the tag (unique, max 50 characters)
    """
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Return the URL to view all posts with this tag.
        """
        return reverse('posts-by-tag', kwargs={'tag_name': self.name})


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
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        Return the URL to access a particular post instance.
        Used by CreateView and UpdateView for redirects after successful form submission.
        """
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
    Comment model representing a comment on a blog post.
    
    Fields:
        post: The blog post this comment belongs to
        author: The user who wrote the comment
        content: The text content of the comment
        created_at: When the comment was created
        updated_at: When the comment was last updated
    """
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The post this comment belongs to'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text='The user who wrote this comment'
    )
    content = models.TextField(
        help_text='The comment text'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the comment was created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the comment was last updated'
    )

    class Meta:
        ordering = ['created_at']  # Oldest comments first
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        indexes = [
            models.Index(fields=['post', 'created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_absolute_url(self):
        """
        Return the URL to the post detail page where this comment appears.
        """
        return reverse('post-detail', kwargs={'pk': self.post.pk})
