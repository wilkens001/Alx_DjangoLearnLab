from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form for CustomUser model.
    Extends Django's UserCreationForm to include additional fields.
    """
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Optional: Enter your date of birth"
    )
    profile_photo = forms.ImageField(
        required=False,
        help_text="Optional: Upload a profile photo"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for CustomUser model.
    Extends Django's UserChangeForm to include additional fields.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django's security features including:
    - CSRF protection (via {% csrf_token %} in template)
    - Input validation and sanitization
    - XSS prevention through automatic output escaping
    
    This form is used in the form_example view to demonstrate secure form handling.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'id': 'name'
        }),
        help_text='Enter your full name'
    )
    
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'id': 'email'
        }),
        help_text='Enter a valid email address'
    )
    
    message = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message...',
            'id': 'message',
            'rows': 5
        }),
        help_text='Enter your message (max 1000 characters)'
    )
    
    def clean_name(self):
        """
        Custom validation for name field.
        Demonstrates input sanitization.
        """
        name = self.cleaned_data.get('name')
        if name:
            # Strip whitespace and validate
            name = name.strip()
            if len(name) < 2:
                raise forms.ValidationError('Name must be at least 2 characters long.')
        return name
    
    def clean_message(self):
        """
        Custom validation for message field.
        Demonstrates input sanitization.
        """
        message = self.cleaned_data.get('message')
        if message:
            # Strip whitespace
            message = message.strip()
            if len(message) < 10:
                raise forms.ValidationError('Message must be at least 10 characters long.')
        return message
