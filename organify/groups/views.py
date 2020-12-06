'''Groups viewsets.'''

# DRF
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

# Models
from users.models import User
from .models import Group, Membership

# Serializers
from .serializers import GroupModelSerializer, MembershipModelSerializer

# Permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsGroupAdmin


import base64
import pathlib


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

    @action(detail=False, methods=['patch'])
    def upload_pic(self, request):


        slug = request.data['slug']
        group = Group.objects.get(slug=slug)


        ext = pathlib.Path(request.FILES['picture'].name).suffix
        ext_final = ext[1:]

        image_file = request.FILES['picture'].open("rb") 
        encoded_string = base64.b64encode(image_file.read())
        string_img = str(encoded_string)
        header_encode = 'data:image/'+ ext_final +';base64,'

        string_img_new = header_encode + string_img[2:-1]

        group.pic = string_img_new
        group.save()

        return Response(status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'])
    def download_pic(self, request):

        pic_bs64 = Groups.objects.get(slug='bestbest').pic

        # Quitr headeradn save string

        ext = pathlib.Path(request.FILES['picture'].name).suffix
        ext_final = ext[1:]

        image_file = request.FILES['picture'].open("rb") 
        encoded_string = base64.b64decode(pic_bas4)
        string_img = str(encoded_string)
        header_encode = 'data:image/'+ ext_final +';base64,'

        string_img_new = header_encode + string_img[2:-1]

        '''Save to DB'''

        # import pdb; pdb.set_trace()

        return Response(status=status.HTTP_200_OK)




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
        '''Must be authenticated for view, add, join or leave groups.'''
        permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_queryset(self):
        '''Return group members.'''
        return Membership.objects.filter(group=self.group)

    def create(self, request, *args, **kwargs):
        '''Join group.'''
        user = self.request.user
        group = self.group # comming from dispatcher method
        membership = Membership(user=user, group=group)
        membership.save()
        # import pdb; pdb.set_trace()
        serializer = MembershipModelSerializer(membership)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)

    # POST /membership/<group_slug>/add_many_members/
    @action(detail=False, methods=['post'])
    def add_many_members(self, request, *args, **kwargs):
        '''Add members to a group by parsing a list of users ids.'''
        uid_list = request.data['id']
        group = self.group # Comming from dispatcher
        membership_list = []
        # import pdb; pdb.set_trace()
        for uid in uid_list:
            user = User.objects.get(id=uid)
            membership_list.append(Membership(user=user, group=group))
        Membership.objects.bulk_create(membership_list)
        return Response(status=status.HTTP_201_CREATED)

    #GET /memberships/<group_slug>/members/
    @action(detail=False, methods=['get'])
    def members(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        group = self.group # Comming from dispatcher
        memberships = Membership.objects.filter(group__slug=group.slug)
        serializer = MembershipModelSerializer(memberships, many=True)
        data = serializer.data
        return Response(data)