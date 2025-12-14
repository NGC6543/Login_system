from django.contrib.auth import logout
from rest_framework import viewsets

from user.models import CustomUser
from .serializers import (
    CustomUserRegisterSerializer, CustomUserReadSerializer,
    CustomUserWriteSerializer, RolePermissionSerializer,
    RoleSerializer, ResourceSerializer
)
from .permissions import IsOwnerOrAdminReadOnly, HasAccessByRole
from user.models import Role, Resource, AccessRoleRule


class UserRegistrationView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegisterSerializer
    http_method_names = ('post',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsOwnerOrAdminReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'patch'):
            return CustomUserWriteSerializer
        return CustomUserReadSerializer

    def perform_destroy(self, instance):
        request = self.request
        instance.is_active = False
        instance.save(update_fields=('is_active',))
        logout(request)


class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = AccessRoleRule.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [HasAccessByRole]


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [HasAccessByRole]


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [HasAccessByRole]
