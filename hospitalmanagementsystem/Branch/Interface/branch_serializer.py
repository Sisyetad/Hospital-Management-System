from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from Role.Interface.role_serializer import RoleSerializer

class BranchSerializer(serializers.Serializer):
    branch_id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    branch_name = serializers.CharField()
    role_name = serializers.SerializerMethodField()
    role = RoleSerializer(write_only=True)
    phone = serializers.CharField()
    speciality = serializers.CharField()
    location = serializers.CharField()
    headoffice_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    def validate(self, data):
        action = self.context.get('action')
        if action == 'create':
            required_fields = ['branch_name', 'email', 'phone', 'speciality', 'location', 'role']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(f"Missing required fields for create: {', '.join(missing_fields)}")
        elif action == 'update':
            update_fields = ['branch_name', 'phone', 'speciality', 'location']
            if not any(data.get(field) for field in update_fields):
                raise serializers.ValidationError("At least one field must be provided for update.")
        return data
    
    @extend_schema_field(str)
    def get_headoffice_name(self, obj):
        return obj.headoffice.headoffice_name if obj.headoffice else None
    
    @extend_schema_field(str)
    def get_role_name(self, obj):
        return obj.role.role_name if obj.role else None