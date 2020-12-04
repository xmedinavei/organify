"""Users URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views as group_views


router = DefaultRouter()
router.register(r'groups', group_views.GroupViewSet, basename='groups')
router.register(r'memberships', group_views.MembershipViewSet, basename='memberships')

urlpatterns = [
    path('', include(router.urls))
]
