from django.db import models
from Branch.Domain.branch_entity import BranchEntity
from Role.Infrastructure.role_model import RoleModel
from Admin.Infrastructure.headoffice_model import HeadofficeModel

class BranchModel(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    headoffice = models.ForeignKey(
        HeadofficeModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='branches'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)


    def to_entity(self):
        return BranchEntity(
            branch_id=self.pk,
            branch_name=self.branch_name,
            email=self.email,
            phone=self.phone,
            location=self.location,
            speciality=self.speciality,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
            headoffice=self.headoffice
        )

    class Meta:
        db_table = 'branch'