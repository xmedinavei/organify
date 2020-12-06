'''Groups models.'''

# Django
from django.db import models


class Group(models.Model):
    '''Group model.
    It is a group which can be created by an logged user. The default number of members is 10.
    The users can join and leave the group.
    '''
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,
                            max_length=50)
    description = models.CharField(max_length=250,
                                   blank=True)
    picture = models.ImageField(upload_to='circles/pictures',
                                blank=True,
                                null=True)
    pic = models.TextField(null=True)
    members = models.ManyToManyField('users.User',
                                     through='groups.Membership',
                                     through_fields=('group', 'user'))
    created = models.DateTimeField(auto_now_add=True,
                                   help_text='Object datetime when created.')
    modified = models.DateTimeField(auto_now=True,
                                    help_text='Object datetime when someone.')

    class Meta:
        '''Meta options.'''
        get_latest_by = 'created'
        ordering = ['-created', '-modified']

    def __str__(self):
        '''Return group name and the slug.'''
        group_name = f'{self.name}, {self.slug}'
        return group_name
    
    
    
class Membership(models.Model):
    '''Membership model.
    Show the user and group relationship and the datetime joined.
    '''
    user = models.ForeignKey('users.User', 
                             on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', 
                              on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False,
                                   help_text='Group admin')
    class Meta:
        '''Meta options.'''
        get_latest_by = 'joined'
        ordering = ['-joined']

    def __str__(self):
        '''Return full membership info.'''
        membership_name = f'Membership id {id} | User: {self.user} | Group: {self.group} | Joined: {self.joined}'
        return membership_name