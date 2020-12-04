'''Organify URL Configuration.'''

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('groups.urls', 'groups'), namespace='groups')),
]
