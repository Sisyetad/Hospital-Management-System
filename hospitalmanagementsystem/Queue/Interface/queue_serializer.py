from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

class QueueSerializer(serializers.Serializer):
    queue_id= serializers.IntegerField(read_only=True)
    patient_id = serializers.IntegerField(write_only=True, required=False)
    status = serializers.IntegerField(required=False)
    doctor_id = serializers.IntegerField(required=False)
    department = serializers.CharField(required=False)
    patient_name = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_patient_name(self, obj):
        return obj.patient.full_name if obj.patient else None

    def validate(self, data):
        action = self.context.get("action")
        if action == 'create':
            if not data.get("patient_id"):
                raise serializers.ValidationError(f"Missing required fields for create: patient_id")
        elif action == 'update':
            if not data.get("status"):
                raise serializers.ValidationError("Give status for update.")
        elif action == 'partial_update':
            if not data.get('doctor_id') and not data.get('department'):
                raise serializers.ValidationError("Give either doctor_id or department for update.")
            
        return data