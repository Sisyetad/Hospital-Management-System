from django.forms import ValidationError

from Role.Infrastructure.role_model import RoleModel
from Role.Domain.role_entity import Role
from ..Domain.role_repo import IRoleRepository


class RoleService:
    def __init__(self, repository: IRoleRepository):
        self.repository =  repository

    def createRole(self, role_name: str)-> Role:
        try:
            return self.repository.createRole(role_name= role_name)
        except ValidationError as e:
            return ValueError(str(e))
    
    def deleteRole(self, role_id)-> bool:
        try:
            return self.repository.deleteRole(role_id= role_id)
        except ValidationError as e:
            return ValueError(str(e))
        
    def updateRole(self, role_id, role_name)-> Role:
        try:
            return self.repository.updateRole(role_id= role_id, role_name= role_name)
        except ValidationError as e:
            return ValueError(str(e))
        
    def getAllRoles(self)-> list[Role]:
        try:
            return self.repository.getAllRoles()
        except ValidationError as e:
            return ValueError(str(e))
