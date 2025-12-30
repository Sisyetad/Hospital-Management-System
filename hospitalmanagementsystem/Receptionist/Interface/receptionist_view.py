from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from User.Permission.role_permissions import DynamicRolePermission
from Receptionist.Application.receptionist_service import ReceptionistService
from Receptionist.Infrastructure.receptionist_repo_imp import ReceptionistRepository
from Receptionist.Interface.receptionist_serializer import ReceptionistSerializer

class ReceptionistViewSet(viewsets.ViewSet):
    serializer_class = ReceptionistSerializer
    lookup_value_regex = r'\d+'
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_service(self, request):
        return ReceptionistService(ReceptionistRepository(current_user=request.user))
    
    def create(self, request):
        """POST /receptionists/"""
        serializer = ReceptionistSerializer(data= request.data, context={"action": "create"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            role = data['role']
            result = service.createReceptionist(
                email=data['email'],
                receptionist_name=data['receptionist_name'],
                role_name=role['role_name'],
                phone=data['phone'],
                location=data['location']
            )
            return Response(ReceptionistSerializer(result).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
    operation_id="receptionists_list",
    responses=ReceptionistSerializer(many=True),
    )
    def list(self, request):
        """GET /receptionists/"""
        try:
            service = self.get_service(request=request)
            result = service.getReceptionistOfBranch()
            serializer = ReceptionistSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="receptionist_retrieve",
        responses=ReceptionistSerializer,
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, pk= None):
        """GET /receptionists/{id}"""
        try:
            service = self.get_service(request=request)
            receptionist = service.getReceptionistByID(pk)
            serializer = ReceptionistSerializer(receptionist)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status= status.HTTP_404_NOT_FOUND)

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
        """PUT /receptionists/{id}"""
        serializer = ReceptionistSerializer(data=request.data, context={"action": "update"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.updateReceptionist(
                receptionist_id=pk,
                receptionist_name=data['receptionist_name'],
                phone=data['phone'],
                location=data['location']
            )
            return Response(ReceptionistSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
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
        """DELETE /receptionists/{id}"""
        try:
            service = self.get_service(request=request)
            service.deleteReceptionist(receptionist_id=pk)
            return Response({"message": "Receptionist deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)