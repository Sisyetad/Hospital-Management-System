from django.db import models
from Patient.Domain.patient_entity import PatientEntity
from Role.Infrastructure.role_model import RoleModel

class PatientModel(models.Model):
    full_name = models.CharField(max_length= 255, unique= True)
    sex = models.CharField(max_length=50)
    phone = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    email = models.EmailField(unique= True)
    role = models.ForeignKey(RoleModel, on_delete= models.CASCADE)
    branch_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default= False)

    def to_entity(self) -> PatientEntity:
        return PatientEntity(
            patient_id= self.pk,
            full_name= self.full_name,
            sex=self.sex,
            phone=self.phone,
            birth_date=self.birth_date,
            email= self.email,
            location=self.location,
            role= self.role,
            branch_name= self.branch_name,
            created_at= self.created_at,
            updated_at= self.updated_at,
            is_active= self.is_active
        )