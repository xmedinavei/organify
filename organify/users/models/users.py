'''User custom models.'''

# Django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Utilities
from utils.models import OrganifyBaseModel


class User(OrganifyBaseModel, AbstractUser):
    '''User model.
    Extends from OrganifyBaseModel and Django AbstractUser.
    We add the email field here and put it as username field.
    '''
    
    email = models.EmailField(unique=True,
                              error_messages={'unique': 'This email already exists.'})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        '''Return id, email, first_name and last_name.'''

        to_show = f'{self.id}, {self.username}, {self.first_name} {self.last_name}'
        return to_show

    def get_short_name(self):
        '''Return the full name. Method in Abstract User.'''

        full_name = f'{self.first_name} {self.last_name}'
        return full_name