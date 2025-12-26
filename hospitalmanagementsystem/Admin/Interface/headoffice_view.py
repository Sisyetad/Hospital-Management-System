from rest_framework import viewsets
from Admin.Interface.headoffice_serializer import HeadofficeSerializer
from Admin.Infrastructure.headoffice_model import HeadofficeModel
from User.Permission.role_permissions import DynamicRolePermission
from rest_framework.permissions import IsAuthenticated

class HeadofficeView(viewsets.ModelViewSet):
    queryset = HeadofficeModel.objects.all()
    serializer_class = HeadofficeSerializer
    permission_classes = [IsAuthenticated, DynamicRolePermission]  
