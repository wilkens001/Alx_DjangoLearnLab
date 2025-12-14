"""
Views for the accounts app.

This module defines API views for user registration, authentication,
and profile management.
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer
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
