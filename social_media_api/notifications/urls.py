"""
URL configuration for the notifications app.

This module defines URL patterns for notification management.
"""

from django.urls import path
from .views import (
    NotificationListView,
    mark_notification_read,
    mark_all_notifications_read
)

app_name = 'notifications'

urlpatterns = [
    # List all notifications for the authenticated user
    # GET /api/notifications/
    path('', NotificationListView.as_view(), name='notification-list'),
    
    # Mark a specific notification as read
    # POST /api/notifications/<int:pk>/read/
    path('<int:pk>/read/', mark_notification_read, name='mark-read'),
    
    # Mark all notifications as read
    # POST /api/notifications/mark-all-read/
    path('mark-all-read/', mark_all_notifications_read, name='mark-all-read'),
]
