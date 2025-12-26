from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from User.Permission.role_permissions import DynamicRolePermission
from Diagnosis.Application.diagnosis_service import DiagnosisService
from Diagnosis.Infrastructure.diagnosis_repo_imp import DiagnosisRepository
from Diagnosis.Interface.diagnosis_serializer import DiagnosisSerializer

class DiagnosisViewSet(viewsets.ViewSet):
    serializer_class = DiagnosisSerializer
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_service(self, request):
        return DiagnosisService(DiagnosisRepository(current_user=request.user))
    
    @extend_schema(
        operation_id="diagnosis_list",
        responses=DiagnosisSerializer(many=True),
    )
    def list(self, request):
        """GET /diagnosis/"""
        serializer = DiagnosisSerializer(data=request.data, context={"action":"list"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.getDiagnoses(patient_id=data['patient_id'])
            serializer = DiagnosisSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        operation_id="diagnosis_retrieve",
        responses=DiagnosisSerializer,
    )
    def retrieve(self, request, pk=None):
        """GET /diagnosis/{pk}"""
        DiagnosisSerializer(context={"action":"retrieve"})
        try:
            service = self.get_service(request=request)
            result = service.getDiagnosis(diagnosis_id=pk)

            return Response(DiagnosisSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        """POST /diagnosis/"""
        serializer = DiagnosisSerializer(data=request.data, context={"action":"create"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.createDiagnosis(
                diagnosis_name=data['diagnosis_name'],
                severity_level=data['severity_level'],
                related_symptomes=data['related_symptomes'],
                clinical_notes=data['clinical_notes'],
                patient_id=data['patient_id'],
                doctor_id=data['doctor_id'],
                medication=data['medication']
            )

            return Response(DiagnosisSerializer(result).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, pk=None):
        """PUT /diagnosis/{pk}/"""
        serializer = DiagnosisSerializer(data=request.data, context={"action":"update"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.updateDiagnosis(
                diagnosis_id=pk,
                severity_level=data['severity_level'],
                related_symptomes=data['related_symptomes'],
                clinical_notes=data['clinical_notes'],
                doctor_id=data['doctor_id'],
                medication=data['medication'],
                updation_reason=data['updation_reason']
            )

            return Response(DiagnosisSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, pk=None):
        """PATCH /diagnosis/{pk}"""
        serializer =DiagnosisSerializer(data=request.data, context={"action":"partial_update"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            visibility = data.get('visibility')
            diagnosis_status = data.get('diagnosis_status')
            if visibility is not None:
                result = service.verify_vissiblity(
                    diagnosis_id=pk
                )
            elif diagnosis_status is not None:
                result = service.updateDiagnosisStatus(diagnosis_id=pk, diagnosis_status=diagnosis_status)
                if diagnosis_status == 3:
                    service.verify_vissiblity(diagnosis_id=pk)
                    
            return Response(DiagnosisSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['get'], url_path='history')
    def display_history(self, request, pk=None):
        """GET /diagnosis/{pk}/history/"""
        try:
            service = self.get_service(request=request)
            history_queryset = service.displayHistory(diagnosis_id=pk)
            
            return Response(history_queryset, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)