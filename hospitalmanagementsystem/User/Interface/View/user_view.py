from User.Application.user_service import UserService
from User.Infrastructure.user_repo_imp import DjangoUserRepository
from User.Interface.Serializer.user_serializer import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from User.Permission.role_permissions import DynamicRolePermission
from drf_spectacular.utils import extend_schema
class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]

    def get_service(self, request):
        return UserService(DjangoUserRepository(request.user))

    @extend_schema(
        operation_id="users_list",
        responses=UserSerializer(many=True),
    )
    def list(self, request):
        """GET /users/"""
        UserSerializer(context={"action": "list"})
        try:
            service = self.get_service(request=request)
            users = service.get_all_users()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        operation_id="users_retrieve",
        responses=UserSerializer,
    )
    def retrieve(self, request, pk=None):
        """GET /users/{id}/"""
        UserSerializer(context={"action": "retrieve"})
        try:
            service = self.get_service(request=request)
            user = service.get_user_by_id(int(pk))
            serializer = UserSerializer(user)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status= status.HTTP_404_NOT_FOUND)
    
    def update(self, request):
        """PUT /users/"""
        try:
            service = self.get_service(request=request)
            serializer = UserSerializer(data=request.data, context= {"action":"update"})
            serializer.is_valid(raise_exception=True)
            user_entity = serializer.to_entity()
            user = service.update_user(user=user_entity)
            return Response(UserSerializer(user).data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """DELETE /users/{id}/"""
        UserSerializer(context={"action": "destroy"})
        try:
            service = self.get_service(request=request)
            service.delete_user(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status= status.HTTP_400_BAD_REQUEST)