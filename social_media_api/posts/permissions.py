"""
Custom permissions for the posts app.

This module defines permissions to ensure users can only modify
their own content.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit or delete their own objects.
    
    - Read permissions (GET, HEAD, OPTIONS) are allowed for any request
    - Write permissions (PUT, PATCH, DELETE) are only allowed to the author
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access this object.
        """
        # Read permissions are allowed for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the object
        return obj.author == request.user
