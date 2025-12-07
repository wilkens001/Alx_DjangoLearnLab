from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form that includes email field.
    Inherits from Django's UserCreationForm and adds email as a required field.
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })

    def save(self, commit=True):
        """
        Save the user instance with the email field.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    Allows users to update their username and email.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def clean_email(self):
        """
        Validate that the email is unique (excluding current user).
        """
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    
    Includes title, content, and tags fields with custom styling.
    The author field is automatically set in the view, not in the form.
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter post title'
        }),
        help_text='Maximum 200 characters'
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your blog post content here...',
            'rows': 10
        }),
        help_text='Write the full content of your blog post'
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags separated by commas (e.g., python, django, web)'
        }),
        help_text='Add tags to categorize your post. Separate multiple tags with commas.'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        # Note: author and published_date are excluded as they're set automatically
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate tags field with existing tags if editing
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def clean_title(self):
        """
        Validate and clean the title field.
        """
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        """
        Validate and clean the content field.
        """
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content
    
    def clean_tags(self):
        """
        Validate and clean the tags field.
        Parse comma-separated tags and validate each tag.
        """
        tags_str = self.cleaned_data.get('tags', '').strip()
        if not tags_str:
            return []
        
        # Split by comma and clean each tag
        tag_names = [tag.strip().lower() for tag in tags_str.split(',') if tag.strip()]
        
        # Validate tag names
        for tag_name in tag_names:
            if len(tag_name) > 50:
                raise forms.ValidationError(f'Tag "{tag_name}" is too long. Maximum 50 characters.')
            if len(tag_name) < 2:
                raise forms.ValidationError(f'Tag "{tag_name}" is too short. Minimum 2 characters.')
        
        return tag_names
    
    def save(self, commit=True):
        """
        Save the post and handle tag creation/assignment.
        """
        instance = super().save(commit=commit)
        
        if commit:
            # Get the cleaned tags
            tag_names = self.cleaned_data.get('tags', [])
            
            # Clear existing tags
            instance.tags.clear()
            
            # Create or get tags and add them to the post
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
        
        return instance


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments on blog posts.
    
    Only includes the content field as post and author are set automatically.
    """
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your comment here...',
            'rows': 4
        }),
        label='Your Comment',
        help_text='Share your thoughts about this post'
    )
    
    class Meta:
        model = Comment
        fields = ['content']
        # Note: post and author are excluded as they're set automatically
    
    def clean_content(self):
        """
        Validate and clean the content field.
        """
        content = self.cleaned_data.get('content')
        if len(content) < 3:
            raise forms.ValidationError('Comment must be at least 3 characters long.')
        if len(content) > 1000:
            raise forms.ValidationError('Comment must not exceed 1000 characters.')
        return content.strip()
