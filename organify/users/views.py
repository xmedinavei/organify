'''Users viewsets'''

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from .serializers import UserModelSerializer, UserSignUpSerializer, UserLoginSerializer

# Models
from .models import User

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAccountOwner


class UserViewSet(viewsets.ModelViewSet):
    '''
    User model view set. 
    For sign up, login, update and delete account.
    '''

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'delete']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]


    # URL: users/signup/
    @action(detail=False, methods=['post'])
    def signup(self, request):
        '''User sign up view using the UserSignUpSerializer.'''
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        
        return Response(data, status=status.HTTP_201_CREATED)

    # URL: users/login/
    @action(detail=False, methods=['post'])
    def login(self, request):
        '''User login.'''
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token,
        }
        return Response(data, status=status.HTTP_200_OK)
