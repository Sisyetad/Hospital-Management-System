from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from Branch.Infrastructure.branch_repo_imp import BranchRepository
from Branch.Application.branch_services import BranchService
from Branch.Interface.branch_serializer import BranchSerializer
from User.Permission.role_permissions import DynamicRolePermission

class BranchViewSet(viewsets.ViewSet):
    serializer_class = BranchSerializer
    lookup_value_regex = r'\d+'
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]

    def get_service(self, request):
        return BranchService(current_user=request.user, repository=BranchRepository(current_user=request.user))

    @extend_schema(
        operation_id="branches_list",
        responses=BranchSerializer(many=True),
    )
    def list(self, request):
        """GET /branches/"""
        BranchSerializer(context={"action": "list"})
        try:
            service = self.get_service(request)
            branches = service.getBranches()
            serializer = BranchSerializer(branches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):
        """POST /branches/"""
        serializer = BranchSerializer(data=request.data, context={'action': 'create'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            role = data.get('role')
            service = self.get_service(request)
            branch = service.createBranch(
                branch_name=data['branch_name'],
                email=data['email'],
                role_name=role['role_name'],
                speciality=data['speciality'],
                phone=data['phone'],
                location=data['location']
            )
            return Response(BranchSerializer(branch).data, status=status.HTTP_201_CREATED)
        except (PermissionDenied, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        """PUT /branches/{pk}/"""
        serializer = BranchSerializer(data=request.data, context={'action': 'update'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            service = self.get_service(request)
            branch = service.updateBranch(
                branch_id=pk,
                branch_name=data.get('branch_name'),
                speciality=data.get('speciality'),
                location=data.get('location'),
                phone=data.get('phone')
            )
            return Response(BranchSerializer(branch).data, status=status.HTTP_200_OK)
        except (PermissionDenied, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        """DELETE /branches/{pk}/"""
        BranchSerializer(context={"action": "destroy"})
        try:
            service = self.get_service(request)
            service.deleteBranch(pk)
            return Response({"message": "Branch deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except (PermissionDenied, ValidationError) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        operation_id="branches_retrieve",
        responses=BranchSerializer,
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, pk=None):
        """GET /branches/{pk}/"""
        BranchSerializer(context={"action": "retrieve"})
        try:
            service = self.get_service(request)
            branch = service.getBranch(pk)
            serializer = BranchSerializer(branch)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)