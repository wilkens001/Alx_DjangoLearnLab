"""
Serializers for the notifications app.

This module defines serializers for the Notification model.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    
    Displays notification details including actor, verb, and target information.
    """
    
    actor = serializers.StringRelatedField(read_only=True)
    actor_id = serializers.IntegerField(source='actor.id', read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)
    recipient_id = serializers.IntegerField(source='recipient.id', read_only=True)
    
    # Simplified target representation
    target_type = serializers.SerializerMethodField()
    target_id = serializers.IntegerField(source='target_object_id', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'recipient_id', 'actor', 'actor_id', 
                  'verb', 'target_type', 'target_id', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'recipient_id', 'actor', 
                           'actor_id', 'timestamp']
    
    def get_target_type(self, obj):
        """
        Get the content type of the target object.
        """
        if obj.target_content_type:
            return obj.target_content_type.model
        return None
