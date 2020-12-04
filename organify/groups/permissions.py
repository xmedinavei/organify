'''Group app custom permissions.'''

# DRF
from rest_framework.permissions import BasePermission

# Models
from .models import Group, Membership


class IsGroupAdmin(BasePermission):
    '''Allow access only to admin group.'''
    
    def has_object_permission(self, request, view, obj):
        '''Verify that request.user is the group admin.'''
        try:
            Membership.objects.get(user=request.user,
                                   group=obj,
                                   is_admin=True)
        except Membership.DoesNotExist:
            False
        return True