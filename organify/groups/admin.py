# Django
from django.contrib import admin
from django.utils.html import format_html

# Model
from .models import Group, Membership

# Utils
import base64


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    '''Group admin.'''
    list_display = ('id', 'name', 'slug', 'description', 
                    'created', 'modified', 'pic_render')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    '''Membership admin.'''
    list_display = ('id', 'user', 'group', 'joined', 'is_admin')
    list_filter = ('group', 'user')
