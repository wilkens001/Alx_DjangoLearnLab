from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


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
    
    Includes title and content fields with custom styling.
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
    
    class Meta:
        model = Post
        fields = ['title', 'content']
        # Note: author and published_date are excluded as they're set automatically
    
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
