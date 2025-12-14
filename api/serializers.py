from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import Role, Resource, AccessRoleRule


CustomUser = get_user_model()


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name',
                  'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class CustomUserReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')


class CustomUserWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'name', 'code']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        fields = ['id', 'name', 'code']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    resource = ResourceSerializer()
    permission = PermissionSerializer()

    class Meta:
        model = AccessRoleRule
        fields = ['id', 'role', 'resource', 'permission']
        extra_kwargs = {
            'role': {'required': True},
            'resource': {'required': True},
            'permission': {'required': True},
        }

    def validate(self, attrs):
        role = attrs.get('role')
        resource = attrs.get('resource')
        permission = attrs.get('permission')

        if AccessRoleRule.objects.filter(
            role=role,
            resource=resource,
            permission=permission
        ).exists():
            raise serializers.ValidationError(
                "This permission is already assigned to this role."
            )

        return attrs
