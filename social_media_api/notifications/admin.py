"""
Admin configuration for the notifications app.

This module registers the Notification model with the Django admin interface.
"""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notification model.
    """
    
    list_display = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'read']
    list_filter = ['read', 'timestamp', 'verb']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('recipient', 'actor', 'verb', 'read')
        }),
        ('Target Information', {
            'fields': ('target_content_type', 'target_object_id')
        }),
        ('Metadata', {
            'fields': ('timestamp',)
        }),
    )
