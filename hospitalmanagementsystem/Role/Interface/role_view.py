from rest_framework.request import Request
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from User.Permission.role_permissions import DynamicRolePermission
from .role_serializer import RoleSerializer
from ..Application.role_service import RoleService
from ..Infrastructure.role_repo_imp import RoleRepository

class RoleView(viewsets.ViewSet):
    serializer_class = RoleSerializer
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_service(self):
        return RoleService(RoleRepository())

    def create(self, request: Request):
        """POST /roles/"""
        serializer = RoleSerializer(data=request.data, context={"action": "create"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = self.get_service()
        try:
            result = service.createRole(
                role_name=data['role_name']
            )
            return Response(
                RoleSerializer(result).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk=None):
        """DELETE /roles/id"""
        service = self.get_service()
        RoleSerializer(context={"action": "destroy"})
        try:
            service.deleteRole(int(pk))
            return Response({"message": "Role deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request: Request):
        """GET /roles/"""
        service = self.get_service()
        RoleSerializer(context={"action": "list"})
        try:
            result = service.getAllRoles()
            return Response(
                [RoleSerializer(role).data for role in result],
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request: Request, pk=None):
        """PUT /roles/id"""
        serializer = RoleSerializer(data=request.data, context={"action": "update"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        service = self.get_service()
        try:
            result = service.updateRole(role_id=pk, role_name=data['role_name'])
            return Response(RoleSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)