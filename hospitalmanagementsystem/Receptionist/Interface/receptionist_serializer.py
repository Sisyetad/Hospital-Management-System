from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from Role.Interface.role_serializer import RoleSerializer

class ReceptionistSerializer(serializers.Serializer):
    receptionist_id = serializers.IntegerField(read_only=True)
    receptionist_name = serializers.CharField(required=False)
    email = serializers.EmailField()
    phone = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    role_name = serializers.SerializerMethodField()
    role=RoleSerializer(write_only=True)
    branch_name = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    @extend_schema_field(str)
    def get_role_name(self, obj):
        return obj.role.role_name if obj.role else None
    
    def validate(self, data):
        action = self.context.get('action')
        if action == 'create':
            required_fields = ['receptionist_name', 'email', 'phone', 'location', 'role']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(f"Missing required fields for create: {', '.join(missing_fields)}")
        elif action == 'update':
            update_fields = ['receptionist_name', 'phone', 'location']
            if not any(data.get(field) for field in update_fields):
                raise serializers.ValidationError("At least one field must be provided for update.")
        return data