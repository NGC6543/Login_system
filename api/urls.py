from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    UserRegistrationView, UserViewSet, RoleViewSet,
    ResourceViewSet, RolePermissionViewSet
)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('signup', UserRegistrationView, basename='register')
v1_router.register('roles', RoleViewSet, basename='roles')
v1_router.register('resources', ResourceViewSet, basename='resources')
v1_router.register(
    'role-permissions', RolePermissionViewSet, basename='role-permissions'
)

urlpatterns = [
    path('', include(v1_router.urls)),
]
