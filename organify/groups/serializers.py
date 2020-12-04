'''Group app serializers.'''

# DRF
from rest_framework import serializers

# Model
from .models import Group, Membership

class GroupSerializer(serializers.ModelSerializer):
    '''Group serilizer to create groups.'''

    class Meta:
        '''Meta options.''' 
        model = Group
        fields = ('id','name', 'slug', 'description', 'picture')


class MembershipSerializer(serializers.ModelSerializer):
    '''Membership serializer to add members to a group.'''

    class Meta:
        '''Meta options.''' 
        model = Membership
        fields = ('id', 'user', 'group')