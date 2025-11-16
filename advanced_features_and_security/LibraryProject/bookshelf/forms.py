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
