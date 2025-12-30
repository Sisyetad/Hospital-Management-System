# users/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTokenLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.TextField(unique=True)
    ip_address = models.GenericIPAddressField()
    device = models.TextField()
    location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default= False)

    def __str__(self):
        return f"{self.user.username} | {self.user.email} | {self.ip_address} | {self.device}"
