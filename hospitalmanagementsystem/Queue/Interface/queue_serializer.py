from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

class QueueSerializer(serializers.Serializer):
    queue_id= serializers.IntegerField(read_only=True)
    patient_id = serializers.IntegerField(write_only=True, required=False)
    status = serializers.IntegerField(required=False)
    doctor_id = serializers.IntegerField(required=False)
    assigned_department = serializers.CharField(required=False)
    patient_name = serializers.SerializerMethodField()
    pid = serializers.CharField(source='patient.pk', read_only=True)
    doctor_name = serializers.SerializerMethodField()

    @extend_schema_field(str)
    def get_patient_name(self, obj):
        return obj.patient.full_name if obj.patient else None
    @extend_schema_field(str)
    def get_doctor_name(self, obj):
        return obj.doctor.doctor_name if obj.doctor else None
    def validate(self, data):
        action = self.context.get("action")
        if action == 'create':
            if 'patient_id' not in data:
                raise serializers.ValidationError(f"Missing required fields for create: patient_id")
        elif action == 'update':
            if 'status' not in data:
                raise serializers.ValidationError("Give status for update.")
        elif action == 'partial_update':
            if 'doctor_id' not in data and 'assigned_department' not in data:
                raise serializers.ValidationError("Give either doctor_id or assigned_department for update.")
            
        return data