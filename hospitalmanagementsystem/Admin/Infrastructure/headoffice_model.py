from django.db import models

from Role.Infrastructure.role_model import RoleModel
from User.Infrastructure.user_model import UserModel
from Admin.Domain.headoffice_entity import HeadofficeEntity


class HeadofficeModel(models.Model):
    headoffice_name = models.CharField(max_length= 255, unique= True)
    email = models.EmailField(unique= True)
    role= models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def to_entity(self) -> HeadofficeEntity:
        return HeadofficeEntity(
            headoffice_id=self.pk,
            user=self.user.to_entity() if hasattr(self.user, "to_entity") else None,
            headoffice_name=self.headoffice_name,
            email=self.email,
            role=self.role.to_entity() if hasattr(self.role, "to_entity") else self.role,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
        )

    class Meta:
        db_table= 'headoffice'