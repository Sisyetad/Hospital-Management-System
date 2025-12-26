from rest_framework import serializers

from ..Domain.role_entity import Role

class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField(read_only = True)
    role_name = serializers.CharField(required = True, max_length = 100)

    def validate(self, data):
        if not data.get('role_name'):
            raise serializers.ValidationError("Role name is required!")
        return data

    def to_entity(self):
        return Role(
            role_id= self.validated_data.get('role_id'),
            name= self.validated_data.get('role_name')
        )