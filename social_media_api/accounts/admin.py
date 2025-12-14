"""
Admin configuration for the accounts app.

This module registers the CustomUser model with the Django admin interface,
providing an interface for managing users.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for CustomUser model.
    
    Extends Django's UserAdmin to include custom fields.
    """
    
    model = CustomUser
    
    # Fields to display in the user list
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'followers_count', 'following_count']
    
    # Add custom fields to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture', 'followers')
        }),
    )
    
    # Add custom fields to the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    
    # Configure the many-to-many widget for followers
    filter_horizontal = ['followers', 'groups', 'user_permissions']


# Register the CustomUser model with the custom admin interface
admin.site.register(CustomUser, CustomUserAdmin)
