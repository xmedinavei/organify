"""User permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    '''Allow acces only to the account owner.'''

    def has_object_permission(self, request, view, obj):
        '''Check obj and user are the same.'''
        return request.user == obj
