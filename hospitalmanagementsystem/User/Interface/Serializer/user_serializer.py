from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from Role.Domain.role_entity import Role
from User.Domain.user_entity import UserEntity
from Role.Interface.role_serializer import RoleSerializer

class UserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    role_name = serializers.SerializerMethodField()
    role = RoleSerializer(write_only=True, required=False)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    @extend_schema_field(str)
    def get_role_name(self, obj):
        return obj.role.role_name if obj.role else None
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        action = self.context.get('action')

        if action == 'signup':
            if not (data.get('username') and data.get('email') and data.get('password')):
                raise serializers.ValidationError("Username, email, and password are required for signup.")
            self.validate_password(data['password'])

        elif action == 'login':
            if not (data.get('email') and data.get('password')):
                raise serializers.ValidationError("Email and password are required for login.")

        elif action == 'logout':
            if not data.get('refresh_token'):
                raise serializers.ValidationError("Refresh token is required for logout.")
            
        elif action == 'update':
            if not (data.get('username') and data.get('password')):
                raise serializers.ValidationError("Username and password are required for update.")
            self.validate_password(data['password'])

        return data

    def to_entity(self):
        return UserEntity(
            user_id=self.validated_data.get("user_id"),
            email=self.validated_data.get("email"),
            username=self.validated_data.get("username", ""),
            password=self.validated_data.get("password", ""),
            role=Role(
                role_id=self.validated_data.get("role", {}).get("role_id", 0),
                role_name=self.validated_data.get("role", {}).get("role_name", "")
            ),
            created_at=self.validated_data.get("created_at"),
            updated_at=self.validated_data.get("updated_at"),
            is_active=self.validated_data.get("is_active", False)
        )

    class Meta:
        ref_name = "AppUser" 