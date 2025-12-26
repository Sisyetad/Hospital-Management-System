from django.db import models
from django.contrib.auth.models import AbstractUser
from Role.Infrastructure.role_model import RoleModel
from ..Domain.user_entity import UserEntity

class UserModel(AbstractUser):
    username= models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def to_entity(self):
        return UserEntity(
            user_id=self.pk,
            username=self.username,
            email=self.email,
            password=None, 
            role=self.role.to_entity(),
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active= self.is_active
        )

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
    
    @property
    def role_name(self):
        return self.role.role_name if self.role else None
