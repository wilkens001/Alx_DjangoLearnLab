"""
Views for the notifications app.

This module defines API views for retrieving and managing notifications.
"""

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    API view for listing user notifications.
    
    GET /api/notifications/
    
    Returns all notifications for the authenticated user,
    with unread notifications prominently displayed (they come first in unread filter).
    
    Query Parameters:
        - unread: Filter for unread notifications only (optional, true/false)
    
    Response:
        - 200 OK: Returns list of notifications
        - 401 Unauthorized: If user is not authenticated
    """
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Return notifications for the authenticated user.
        Can filter by unread status.
        """
        user = self.request.user
        queryset = Notification.objects.filter(recipient=user)
        
        # Filter by unread if specified
        unread_param = self.request.query_params.get('unread', None)
        if unread_param and unread_param.lower() == 'true':
            queryset = queryset.filter(read=False)
        
        return queryset


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, pk):
    """
    Mark a notification as read.
    
    POST /api/notifications/<int:pk>/read/
    
    Marks the specified notification as read for the authenticated user.
    
    Response:
        - 200 OK: Notification marked as read
        - 404 Not Found: Notification doesn't exist or doesn't belong to user
    """
    notification = get_object_or_404(
        Notification, 
        pk=pk, 
        recipient=request.user
    )
    
    notification.mark_as_read()
    
    serializer = NotificationSerializer(notification)
    return Response({
        'message': 'Notification marked as read',
        'notification': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the authenticated user.
    
    POST /api/notifications/mark-all-read/
    
    Response:
        - 200 OK: All notifications marked as read
    """
    user = request.user
    unread_count = Notification.objects.filter(
        recipient=user, 
        read=False
    ).update(read=True)
    
    return Response({
        'message': f'{unread_count} notification(s) marked as read'
    }, status=status.HTTP_200_OK)
