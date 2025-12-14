"""
Models for the Notifications system in the Social Media API.

This module defines the Notification model for tracking user interactions
and activities within the platform.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Notification(models.Model):
    """
    Notification model for tracking user interactions and activities.
    
    Uses GenericForeignKey to reference any model type as the target
    of the notification (e.g., Post, Comment, User for follows).
    
    Attributes:
        recipient (ForeignKey): User receiving the notification
        actor (ForeignKey): User who performed the action
        verb (CharField): Description of the action (e.g., "liked your post")
        target_content_type (ForeignKey): ContentType of the target object
        target_object_id (PositiveIntegerField): ID of the target object
        target (GenericForeignKey): The actual target object
        timestamp (DateTimeField): When the notification was created
        read (BooleanField): Whether the notification has been read
    """
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User receiving the notification"
    )
    
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='actor_notifications',
        help_text="User who performed the action"
    )
    
    verb = models.CharField(
        max_length=255,
        help_text="Description of the action"
    )
    
    # GenericForeignKey setup for target
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Content type of the target object"
    )
    
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the target object"
    )
    
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the notification was created"
    )
    
    read = models.BooleanField(
        default=False,
        help_text="Whether the notification has been read"
    )
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['recipient', 'read']),
        ]
    
    def __str__(self):
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark the notification as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])
