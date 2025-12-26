from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from User.Permission.role_permissions import DynamicRolePermission
from Queue.Application.queue_service import QueueService
from Queue.Infrastructure.queue_repo_imp import QueueRepository
from Queue.Interface.queue_serializer import QueueSerializer
from drf_spectacular.utils import extend_schema
class QueueViewSet(viewsets.ViewSet):
    serializer_class = QueueSerializer
    def get_permissions(self):
        return [IsAuthenticated(), DynamicRolePermission()]
    
    def get_service(self, request):
        return QueueService(QueueRepository(current_user=request.user))
    
    def create(self, request):
        """POST /queues/"""
        serializer = QueueSerializer(data=request.data, context={"action":"create"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.createQueue(patient_int=data['patient_id'])
            return Response(QueueSerializer(result).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
    @extend_schema(
        operation_id="queues_list",
        responses=QueueSerializer(many=True),
    )  
    def list(self, request):
        """GET /queues/"""
        QueueSerializer(context={"action":"list"})
        try:
            service = self.get_service(request=request)
            result = service.getQueues()
            serializer = QueueSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @extend_schema(
        operation_id="queues_retrieve",
        responses=QueueSerializer,
    )
    def retrieve(self, request, pk=None):
        """GET/queues/{pk}"""
        QueueSerializer(context={"action":"retrieve"})
        try:
            service = self.get_service(request=request)
            result = service.getQueue(queue_id=pk)
            return Response(QueueSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
    
        
    def destroy(self, request, pk=None):
        """DELETE /queues/{pk}"""
        QueueSerializer(context={"action":"destroy"})
        try:
            service = self.get_service(request=request)
            service.deleteQueue(queue_id=pk)
            return Response({"message":"Queue delete successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def partial_update(self, request, pk=None):
        """PATCH /patients/{pk}"""
        serializer = QueueSerializer(
            data=request.data,
            context={'action': 'partial_update'},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            service = self.get_service(request=request)
            doctor_id = data.get('doctor_id')
            department = data.get('assigned_department')

            if doctor_id is not None:
                result = service.assignPatientToDoctor(queue_id=pk, doctor_id=doctor_id)
            elif department is not None:
                result = service.assignPatientToDepartment(queue_id=pk, department=department)
            else:
                return Response(
                    {"error": "Either 'doctor_id' or 'assigned_department' must be provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(QueueSerializer(result).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT /queues/{pk}"""
        serializer = QueueSerializer(data=request.data, context={"action":"update"})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            service = self.get_service(request=request)
            result = service.updateQueue(queue_id=pk, status=data['status'])
            return Response(QueueSerializer(result).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)