# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from .models import User



class CustomUserAdmin(UserAdmin):
    '''Customer User model admin.'''

    list_display = ('id','email', 'username', 'first_name',
                    'last_name', 'password', 'is_active')
    list_filter = ('is_active',)
    ordering = ['-id']

admin.site.register(User, CustomUserAdmin)