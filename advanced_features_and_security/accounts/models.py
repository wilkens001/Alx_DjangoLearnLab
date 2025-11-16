from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    """Custom manager extending Django's UserManager to ensure compatibility
    with Django's createsuperuser and create_user flows while allowing
    extra fields to be passed through.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        # Accept date_of_birth and profile_photo in extra_fields if provided
        if not username:
            raise ValueError('The given username must be set')
        return super().create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return super().create_superuser(username=username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser with additional fields:
    - date_of_birth: optional DateField
    - profile_photo: optional ImageField

    Uses CustomUserManager as objects manager.
    """

    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.get_username()
