from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from User.Permission.role_permissions import DynamicRolePermission
from Patient.Application.patient_service import PatientService
from Patient.Infrastructure.patient_repo_imp import PatientRepository
from Patient.Interface.patient_serializer import PatientSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

class PatientViewSet(viewsets.ViewSet):
    serializer_class = PatientSerializer
    lookup_value_regex = r'\d+'
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_service(self, request):
        return PatientService(PatientRepository(request.user))

    @extend_schema(
        operation_id="patients_list",
        responses=PatientSerializer(many=True),
    )
    def list(self, request):
        """GET /patients/"""
        PatientSerializer(context={'action': 'list'})
        try:
            service = self.get_service(request=request)
            result = service.getPatients()
            patients = PatientSerializer(result, many=True)
            return Response(patients.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(
        operation_id="patients_retrieve",
        responses=PatientSerializer,
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, pk=None):
        """Get /patients/{pk}"""
        PatientSerializer(context={'action': 'retrieve'})
        try:
            service = self.get_service(request=request)
            patient = service.getPatientByID(patient_id=pk)
            return Response(PatientSerializer(patient).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        """POST /patients/"""
        serializer = PatientSerializer(data=request.data, context={'action': 'create'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.createPatient(
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                location=data['location'],
                sex=data['sex'],
                birth_date=data['birth_date'],
                role_name=data['role']['role_name']
            )

            return Response(PatientSerializer(result).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, pk=None):
        """PUT /patients/{pk}"""
        serializer = PatientSerializer(data=request.data, context={'action': 'update'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.updatePatient(
                patient_id=pk,
                full_name=data['full_name'],
                email=data['email'],
                birth_date=data['birth_date'],
                phone=data['phone'],
                location=data['location'],
                sex=data['sex']
            )
            return Response(PatientSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, pk=None):
        """DELETE /patients/{pk}"""
        PatientSerializer(context={'action': 'destroy'})
        try:
            service = self.get_service(request=request)
            service.deletePatient(patient_id=pk)
            return Response({"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)