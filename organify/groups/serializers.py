'''Group app serializers.'''
# Django
from django.core.mail import EmailMultiAlternatives

# DRF
from rest_framework import serializers

# Model
from users.models import User
from .models import Group, Membership

# Serializers
from users.serializers import UserModelSerializer


class GroupModelSerializer(serializers.ModelSerializer):
    '''Group serilizer to create groups.'''

    class Meta:
        '''Meta options.''' 
        model = Group
        fields = ('id','name', 'slug', 'description', 'picture', 'pic')

    def create(self, data):
        group = Group.objects.create(**data)
        self.send_email_to_superusers(group)
        return group

    def send_email_to_superusers(self, group):
        '''Send email to superusers when a group is created.'''
        superusers = User.objects.filter(is_superuser=True)
        # import pdb; pdb.set_trace()
        subject = 'A new group have been created!'
        content = f'A group called "{group.name}" have been created.'
        from_email = 'noreply@organify.com'
        to_email = [su.email for su in superusers]
        msg = EmailMultiAlternatives(subject, content, from_email, to_email)
        msg.send()




class MembershipModelSerializer(serializers.ModelSerializer):
    '''Membership serializer to add members to a group.'''

    user = UserModelSerializer(read_only=True)
    group = GroupModelSerializer(read_only=True)

    class Meta:
        '''Meta options.''' 
        model = Membership
        fields = ('id', 'user', 'group', 'joined')