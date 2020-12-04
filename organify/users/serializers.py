'''Users serializers.'''
#Django
from django.contrib.auth import password_validation, authenticate

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

# Models
from .models import User

class UserModelSerializer(serializers.ModelSerializer):
    '''User model serializer.'''

    # profile = ProfileModelSerializer(read_only=True)

    class Meta:
        '''Meta class.'''

        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class UserSignUpSerializer(serializers.Serializer):
    '''User signup serializer.'''

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(min_length=4,
                                     max_length=24,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(min_length=2,
                                       max_length=24)
    last_name = serializers.CharField(min_length=2,
                                      max_length=24)
    password = serializers.CharField(min_length=6, 
                                     max_length=64)
    password_confirmation = serializers.CharField(min_length=6,
                                                  max_length=64)

    def validate(self, data):
        '''Check that passwords match.'''

        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match.')
        # Django checks whther password id valid
        password_validation.validate_password(password)
        return data

    def create(self, data):
        '''Create the user.'''

        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        # Profile.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    '''User login serializer.'''

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,
                                     max_length=64)
                                     
    def validate(self, data):
        """Check credentials."""
        
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('Account is inactive.')
        self.context['user'] = user
        return data

    def create(self, data):
        '''Generate or retrieve token.'''
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key