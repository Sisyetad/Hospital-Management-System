from django.db import models

from Role.Infrastructure.role_model import RoleModel

# Create your models here.
class HeadofficeModel(models.Model):
    headoffice_name = models.CharField(max_length= 255, unique= True)
    email = models.EmailField(unique= True)
    role= models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table= 'headoffice'