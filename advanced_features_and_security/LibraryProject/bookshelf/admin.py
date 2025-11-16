from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for the CustomUser model"""
    # Display these fields in the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # Add search capability for these fields
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Add filters in the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Order entries by username by default
    ordering = ('username',)
    
    # Define fieldsets for the user detail/edit page
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )
    
    # Define fieldsets for the add user page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo'),
        }),
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for the Book model"""
    # Display these fields in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add search capability for these fields
    search_fields = ['title', 'author']
    
    # Add filters in the right sidebar
    list_filter = ('publication_year', 'author')
    
    # Order entries by title by default
    ordering = ('title',)
