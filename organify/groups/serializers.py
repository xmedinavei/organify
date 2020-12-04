'''Group app serializers.'''

# DRF
from rest_framework import serializers

# Model
from .models import Group, Membership

# Serializers
from users.serializers import UserModelSerializer


class GroupModelSerializer(serializers.ModelSerializer):
    '''Group serilizer to create groups.'''

    class Meta:
        '''Meta options.''' 
        model = Group
        fields = ('id','name', 'slug', 'description', 'picture')


class MembershipModelSerializer(serializers.ModelSerializer):
    '''Membership serializer to add members to a group.'''

    user = UserModelSerializer(read_only=True)
    group = GroupModelSerializer(read_only=True)

    class Meta:
        '''Meta options.''' 
        model = Membership
        fields = ('id', 'user', 'group', 'joined')