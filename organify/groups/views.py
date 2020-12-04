'''Groups viewsets.'''

# DRF
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models
from .models import Group, Membership

# Serializers
from .serializers import GroupModelSerializer, MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGroupAdmin


class GroupViewSet(viewsets.ModelViewSet):
    '''Group view set. We can Create, update and delete groups.'''
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
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
    '''Groups memberships. To view, add or leave groups.'''

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        '''Get the group slug from the URL and put it to the attributes.'''
        # import pdb; pdb.set_trace()
        slug = kwargs['slug']
        self.group = get_object_or_404(Group, slug=slug)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        '''Must be authenticated for view, join or leave groups.'''
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        '''Return group members.'''
        return Membership.objects.filter(group=self.group)

    def create(self, request, *args, **kwargs):

        user = self.request.user
        group = self.group # comming from dispatcher method
        membership = Membership(user=user, group=group)
        membership.save()
        # import pdb; pdb.set_trace()
        serializer = MembershipModelSerializer(membership)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)