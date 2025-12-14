from rest_framework import permissions

from user.models import Role, AccessRoleRule


class IsOwnerOrAdminReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_permission(self, request, view):
        return (request.user.is_staff
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(
           request.user.is_admin or (obj == request.user)
        )


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return (
            user.is_authenticated and
            (user.is_staff or user.is_admin or user.is_superuser)
        )


class HasAccessByRole(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        element_code = getattr(view, 'Resource', None)
        action = view.action

        return self._check_access(request, element_code, action)

    def _check_access(self, request, element_code, action):
        user = request.user

        roles = Role.objects.filter(userrole__user=user)

        rules = AccessRoleRule.objects.filter(
            role__in=roles,
            element__code=element_code
        )

        if action in ['list', 'retrieve']:
            return rules.filter(
                read_permission=True
            ).exists()

        if action == 'create':
            return rules.filter(create_permission=True).exists()

        if action in ['update', 'partial_update']:
            return rules.filter(update_permission=True).exists()

        if action == 'destroy':
            return rules.filter(delete_permission=True).exists()

        return False
