from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Role, AccessRoleRule, Resource, UserRole


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    model = User

    list_display = ('pk', 'email', 'username', 'first_name')


class RoleAdmin(admin.ModelAdmin):
    model = Role

    list_display = ('pk', 'name')


class ResourceAdmin(admin.ModelAdmin):
    model = Resource

    list_display = ('pk', 'name', 'code')


class AccessRoleRuleAdmin(admin.ModelAdmin):
    model = AccessRoleRule

    list_display = ('pk', 'role', 'element')


class UserRoleAdmin(admin.ModelAdmin):
    model = UserRole

    list_display = ('pk', 'user', 'role')


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(AccessRoleRule, AccessRoleRuleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
