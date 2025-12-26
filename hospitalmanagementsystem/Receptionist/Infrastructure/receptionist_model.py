from django.db import models
from Receptionist.Domain.receptionist_entity import ReceptionistEntity
from Role.Infrastructure.role_model import RoleModel
from Branch.Infrastructure.branch_model import BranchModel

class ReceptionistModel(models.Model):
    receptionist_name = models.CharField(max_length= 255, unique= True)
    email = models.EmailField(unique= True)
    phone= models.CharField(unique= True, max_length= 255)
    location= models.CharField(max_length=255)
    role = models.ForeignKey(RoleModel, on_delete= models.CASCADE)
    branch= models.ForeignKey(BranchModel, on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default= False)

    def to_entity(self) -> ReceptionistEntity:
        return ReceptionistEntity(
            receptionist_id= self.id,
            receptionist_name= self.receptionist_name,
            email= self.email,
            phone= self.phone,
            location= self.location,
            role= self.role,
            branch= self.branch,
            created_at= self.created_at,
            updated_at= self.updated_at,
            is_active= self.is_active
        )