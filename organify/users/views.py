'''Users viewsets'''

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Permissions
from rest_framework.permissions import IsAuthenticated, AllowAny

# Serializers
from .serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    UserLoginSerializer,
    # ProfileModelSerializer,
)

# Models
from .models import User

class UserViewSet(viewsets.ModelViewSet):
    '''
    User model view set. 
    For sign up, login and delete account.
    '''

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'

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

    # URL: users/delete/
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        '''Inactive user account'''
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data['email'])
        user.delete()
        # import pdb; pdb.set_trace()
        data = {
            'user': UserModelSerializer(user).data
        }
        return Response(data, status=status.HTTP_200_OK)
