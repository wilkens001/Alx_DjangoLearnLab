"""
Views for the accounts app.

This module defines API views for user registration, authentication,
and profile management.
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
# Example usage: generics.GenericAPIView, CustomUser.objects.all()
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    UserFollowSerializer
)

# Get the custom user model
User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API view for user registration.
    
    POST /api/register/
    
    Request body:
        - username (required): Unique username
        - email (required): User email address
        - password (required): User password
        - password_confirm (required): Password confirmation
        - bio (optional): User biography
        - profile_picture (optional): Profile picture file
    
    Response:
        - 201 Created: Returns user data and authentication token
        - 400 Bad Request: Returns validation errors
    """
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user and return user data with authentication token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Get the token for the newly created user
        token = Token.objects.get(user=user)
        
        # Return user data with token
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'bio': user.bio,
            },
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API view for user login.
    
    POST /api/login/
    
    Request body:
        - username (required): User's username
        - password (required): User's password
    
    Response:
        - 200 OK: Returns user data and authentication token
        - 400 Bad Request: Returns error if credentials are invalid
    """
    
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        """
        Authenticate user and return authentication token.
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'bio': user.bio,
                },
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid username or password'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating user profile.
    
    GET /api/profile/
    - Returns authenticated user's profile information
    
    PUT/PATCH /api/profile/
    - Updates authenticated user's profile
    
    Request body (for update):
        - email (optional): New email address
        - first_name (optional): First name
        - last_name (optional): Last name
        - bio (optional): Biography
        - profile_picture (optional): Profile picture file
    
    Response:
        - 200 OK: Returns user profile data
        - 401 Unauthorized: If user is not authenticated
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """
        Return the authenticated user's profile.
        """
        return self.request.user
    
    def get_serializer_class(self):
        """
        Use different serializer for update operations.
        """
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer


class UserListView(generics.ListAPIView):
    """
    API view for listing all users.
    
    GET /api/users/
    
    Response:
        - 200 OK: Returns list of all users
    """
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetailView(generics.RetrieveAPIView):
    """
    API view for retrieving a specific user's profile.
    
    GET /api/users/<int:pk>/
    
    Response:
        - 200 OK: Returns user profile data
        - 404 Not Found: If user doesn't exist
    """
    
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user.
    
    POST /api/follow/<int:user_id>/
    
    Allows authenticated user to follow another user.
    Users cannot follow themselves.
    
    Response:
        - 200 OK: User followed successfully
        - 400 Bad Request: If trying to follow self or already following
        - 404 Not Found: If user doesn't exist
    """
    user_to_follow = get_object_or_404(User, id=user_id)
    current_user = request.user
    
    # Check if trying to follow self
    if user_to_follow == current_user:
        return Response({
            'error': 'You cannot follow yourself'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already following
    if current_user.following.filter(id=user_id).exists():
        return Response({
            'error': f'You are already following {user_to_follow.username}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Add to following
    current_user.following.add(user_to_follow)
    
    # Create notification for the followed user
    from notifications.models import Notification
    Notification.objects.create(
        recipient=user_to_follow,
        actor=current_user,
        verb='started following you',
        target_content_type=ContentType.objects.get_for_model(user_to_follow),
        target_object_id=user_to_follow.id
    )
    
    serializer = UserFollowSerializer(user_to_follow)
    return Response({
        'message': f'You are now following {user_to_follow.username}',
        'user': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user.
    
    POST /api/unfollow/<int:user_id>/
    
    Allows authenticated user to unfollow another user.
    
    Response:
        - 200 OK: User unfollowed successfully
        - 400 Bad Request: If not following the user
        - 404 Not Found: If user doesn't exist
    """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    current_user = request.user
    
    # Check if following the user
    if not current_user.following.filter(id=user_id).exists():
        return Response({
            'error': f'You are not following {user_to_unfollow.username}'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Remove from following
    current_user.following.remove(user_to_unfollow)
    
    serializer = UserFollowSerializer(user_to_unfollow)
    return Response({
        'message': f'You have unfollowed {user_to_unfollow.username}',
        'user': serializer.data
    }, status=status.HTTP_200_OK)
