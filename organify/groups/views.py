'''Groups viewsets.'''

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from .models import Group, Membership

# Serializers
from .serializers import GroupSerializer, MembershipSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGroupAdmin


class GroupViewSet(viewsets.ModelViewSet):
    '''Group view set. We can Create, update and delete groups.'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = 'slug'
    ordering = ('-modified', '-created')

    def get_permissions(self):
        '''Must be authenticated to perform any view here,
        but only group admins can update and delete.'''
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy', 'delete']:
            permissions.append(IsGroupAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        '''The user who create the group is group admin.'''
        group = serializer.save()
        # import pdb; pdb.set_trace()
        user = self.request.user
        Membership.objects.create(user=user,
                                  group=group,
                                  is_admin=True)

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        '''Inactive group account'''
        group_name = request.data['name']
        slug = request.data['slug']
        group = Group.objects.get(slug=slug)
        group.delete()
        # import pdb; pdb.set_trace()
        data = {
            'Deleted': f'Name: {group_name} Slug: {slug}'
        }
        return Response(data, status=status.HTTP_200_OK)



class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer