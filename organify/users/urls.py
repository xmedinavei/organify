"""Users URLs."""

# Django
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from . import views as user_views


router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls))
]+ static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
