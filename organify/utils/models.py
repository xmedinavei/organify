'''Project models utilities.'''

# Django
from django.db import models


class OrganifyBaseModel(models.Model):
    '''Organify base abstract model.
    This will be the base that other project models will inherit. 
    They will inherit the created (DateTime) and modified (DateTime) attributes.
    '''

    created = models.DateTimeField(auto_now_add=True,
                                   help_text='Object datetime when created.')

    modified = models.DateTimeField(auto_now=True,
                                    help_text='Object datetime when modified.')

    class Meta:
        '''Meta options.'''
        
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']