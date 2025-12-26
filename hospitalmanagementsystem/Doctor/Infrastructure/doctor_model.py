from django.db import models
from Branch.Infrastructure.branch_model import BranchModel
from Doctor.Domain.doctor_entity import DoctorEntity
from Role.Infrastructure.role_model import RoleModel

class DoctorModel(models.Model):
    doctor_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, default='+251')
    location = models.CharField(max_length=255, default='None')
    branch = models.ForeignKey(BranchModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_available = models.BooleanField(default=False)

    def to_entity(self):
        return DoctorEntity(
            doctor_id=self.pk,
            doctor_name=self.doctor_name,
            email=self.email,
            phone= self.phone,
            location= self.location,
            role= self.role.to_entity(),
            department=self.department,
            branch= self.branch.to_entity(),
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            is_available=self.is_available
        )

    class Meta:
        db_table = 'doctor'