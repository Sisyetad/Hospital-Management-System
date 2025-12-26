from django.contrib import admin

from .Infrastructure.token_model import AuthTokenLog
from .Infrastructure.user_model import UserModel
# Register your models here.

admin.site.register(AuthTokenLog)

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)
