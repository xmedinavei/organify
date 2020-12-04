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
    description = models.CharField(max_length=250)
    picture = models.ImageField(upload_to='circles/pictures',
                                blank=True,
                                null=True)
    members = models.ManyToManyField('users.User',
                                     through='groups.Membership',
                                     through_fields=('group', 'user'))
    
class Membership(models.Model):
    '''Membership model.
    Show the user and group relationship and the datetime joined.
    '''
    
    user = models.ForeignKey('users.User', 
                             on_delete=models.CASCADE)
    group = models.ForeignKey('groups.Group', 
                              on_delete=models.CASCADE)
    joined = models.DateTimeField(auto_now_add=True)