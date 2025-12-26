from django.forms import ValidationError
from rest_framework import status,viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from Doctor.Application.command_service import DoctorCommandService
from Doctor.Application.query_service import DoctorQueryService
from Doctor.Infrastructure.doctor_repo_imp import DoctorRepository
from Doctor.Interface.doctor_serializer import DoctorSerializer
from User.Permission.role_permissions import DynamicRolePermission
from Branch.Infrastructure.branch_repo_imp import BranchRepository
from Role.Infrastructure.role_repo_imp import RoleRepository

class DoctorViewSet(viewsets.ViewSet):
    serializer_class = DoctorSerializer
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_command_service(self, request):
        return DoctorCommandService(doctor_repo=DoctorRepository(), branch_repo=BranchRepository(current_user=request.user), role_repo=RoleRepository(), current_user= request.user)

    def get_query_service(self, request):
        return DoctorQueryService(DoctorRepository())
    
    def create(self, request: Request):
        """POST /doctors/"""
        serializer = DoctorSerializer(data=request.data, context={'action': 'create'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            role = data['role']
            service = self.get_command_service(request)
            result = service.create_doctor(
                doctor_name=data['doctor_name'],
                email=data['email'],
                role_name=role['role_name'],
                department=data['department'],
                phone=data['phone'],
                location=data['location'],
            )
            return Response(DoctorSerializer(result).data, status=status.HTTP_201_CREATED)
        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request: Request, pk=None):
        """DELETE /doctors/{pk}"""
        DoctorSerializer(context={"action": "destroy"})
        try:
            service = self.get_command_service(request)
            service.delete_doctor(pk)
            return Response({"message": "Doctor deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request: Request, pk=None):
        """PUT /doctors/{pk}"""
        serializer = DoctorSerializer(data=request.data, context={'action': 'update'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_command_service(request)
            result = service.update_doctor(
                doctor_id=pk,
                doctor_name=data['doctor_name'],
                role_name=data['role']['role_name'],
                department=data['department'],
                phone=data['phone'],
                location=data['location'],
            )
            return Response(DoctorSerializer(result).data, status=status.HTTP_200_OK)
        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        operation_id="doctors_retrieve",
        responses=DoctorSerializer,
    )
    def retrieve(self, request: Request, pk= None):
        """GET /doctors/{pk}"""
        DoctorSerializer(context={"action": "retrieve"})
        try:
            service = self.get_query_service(request)
            result = service.get_doctor(doctor_id=pk)
            return Response(DoctorSerializer(result).data, status=status.HTTP_200_OK)

        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        operation_id="doctors_list",
        responses=DoctorSerializer(many=True),
    )
    def list(self, request):
        """GET /doctors/{branch_id}"""
        DoctorSerializer(context={"action": "list"})
        branch_id = request.query_params.get('branch_id', None)
        try:
            service = self.get_query_service(request)
            if branch_id:
                doctors = service.get_doctors_of_branch(branch_id=branch_id)
            else:
                doctors = service.get_all_doctors(all='all')
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def partial_update(self, request: Request, pk=None):
        """PATCH /doctors/{id}/"""
        try:
            service = self.get_command_service(request)
            doctor = self.get_query_service(request=request).get_doctor(doctor_id=pk)

            if doctor.email != request.user.email:
                raise PermissionDenied("You are not allowed to update other doctor's profile.")
            
            serializer = DoctorSerializer(doctor, data=request.data, context={'action': 'partial_update'}, partial=True)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            updated_doctor = service.update_doctor_status(status=data["is_available"])

            return Response(DoctorSerializer(updated_doctor).data, status=status.HTTP_200_OK)

        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], url_path=r'(?P<branch_id>[^/.]+)/available')
    def list_available_doctors(self, request, branch_id=None):
        """GET /doctors/{branch_id}/available/"""
        DoctorSerializer(context={"action": "list_available_doctors"})
        try:
            service = self.get_query_service(request)
            doctors = service.get_available_doctors(branch_id=branch_id)
            
            for doc in doctors:
                print(f"Doctor: {doc.doctor_name}, is_available: {doc.is_available} (type: {type(doc.is_available)})")
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValidationError, PermissionDenied) as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)