from rest_framework import serializers

class DiagnosisSerializer(serializers.Serializer):
    diagnosis_id = serializers.IntegerField(read_only=True)
    diagnosis_name = serializers.CharField(required=False)
    patient_id = serializers.IntegerField(required=False)
    doctor_id = serializers.IntegerField(required=False)
    medication = serializers.CharField(required=False)
    clinical_notes = serializers.CharField(required=False)
    severity_level = serializers.IntegerField(required=False)
    related_symptomes = serializers.CharField(required=False)
    updation_reason = serializers.CharField(required=False)
    visibility = serializers.BooleanField(required=False)
    diagnosis_status = serializers.IntegerField(required=False)

    def validate(self, data):
        action = self.context.get('action')
        if action == 'create':
            required_fields = ['diagnosis_name', 'severity_level', 'related_symptomes', 'clinical_notes', 'patient_id','medication']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(f"Missing required fields for create usecase:{', '.join(missing_fields)}")
        if action == 'update':
            required_fields = ['severity_level', 'related_symptomes', 'clinical_notes', 'doctor_id', 'medication', 'updation_reason']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                raise serializers.ValidationError(f"Missing fields for update diagnosis: {', '.join(missing_fields)}")
        if action == 'list':
            if not data.get('patient_id'):
                raise serializers.ValidationError("Missing field for list the diagnosis: patient_id.")
        if action == 'partial_update':
            if data.get('visibility') is None and data.get('diagnosis_status') is None:
                raise serializers.ValidationError("Missing field for partial_update the diagnosis.")
            
        return data
    
