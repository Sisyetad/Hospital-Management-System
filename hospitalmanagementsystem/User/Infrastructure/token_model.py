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


from django.db import models
from django.conf import settings

class AuditLogModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.PositiveIntegerField()
    user_agent = models.TextField(blank=True)
    device = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    browser = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_mobile = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user or 'anon'} {self.path} {self.status_code}"