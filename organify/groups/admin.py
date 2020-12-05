# Djnago
from django.contrib import admin

# Model
from .models import Group, Membership


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    '''Group admin.'''
    list_display = ('id', 'name', 'slug', 'description', 
                    'picture', 'created', 'modified')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    '''Membership admin.'''
    list_display = ('id', 'user', 'group', 'joined', 'is_admin')
    list_filter = ('group', 'user')