from django.db import models

from ..Domain.role_entity import Role

class RoleModel(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name
    
    def to_entity(self):
        return Role(role_id=self.id, role_name=self.role_name)
    
    class Meta:
        db_table = 'role'