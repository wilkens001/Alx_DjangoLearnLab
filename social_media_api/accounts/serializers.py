"""
Serializers for the accounts app.

This module defines serializers for user registration, authentication,
and profile management using Django REST Framework.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Get the custom user model
User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles the creation of new user accounts with password validation.
    Returns an authentication token upon successful registration.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="User password (will be hashed)"
    )
    
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Confirm password"
    )
    
    token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 
                  'bio', 'profile_picture', 'token']
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password': 'Passwords do not match.'
            })
        return data
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password and return auth token.
        """
        # Remove password_confirm from validated data
        validated_data.pop('password_confirm')
        
        # Create user using create_user method (handles password hashing)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        
        # Create authentication token for the user
        Token.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Validates user credentials and returns authentication token.
    """
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(read_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data.
    
    Provides detailed user information including followers and following counts.
    """
    
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    following = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                  'bio', 'profile_picture', 'date_joined', 
                  'followers_count', 'following_count', 'followers', 'following']
        read_only_fields = ['id', 'username', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    
    Allows users to update their profile information.
    """
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_picture']
        extra_kwargs = {
            'email': {'required': False},
        }
