from Role.Domain.role_entity import Role
from .role_model import RoleModel
from ..Domain.role_repo import IRoleRepository
from django.core.exceptions import ValidationError


class RoleRepository(IRoleRepository):
    def createRole(self, role_name)-> Role:
        role_model = RoleModel.objects.create(role_name = role_name)
        return role_model.to_entity()
    
    def deleteRole(self, role_id)-> bool:
        try:
            role = RoleModel.objects.get(pk = role_id)
            role.delete()
            return True
        except RoleModel.DoesNotExist:
            return False
    
    def updateRole(self, role_id, role_name)-> Role:
        try:
            role = RoleModel.objects.get(pk = role_id)
            role.name = role_name
            return role.to_entity()
        except RoleModel.DoesNotExist:
            return ValidationError("Invalid role ID.")
    
    def getAllRoles(self)-> list[Role]:
        return [role.to_entity() for role in  RoleModel.objects.all()]
    
    def getRole(self, role_name)-> Role:
        try:
            role = RoleModel.objects.get(role_name=role_name)
            return role.to_entity()
        except RoleModel.DoesNotExist:
            return ValidationError("Role not found.")