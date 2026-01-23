from django.contrib import admin

from .Infrastructure.token_model import AuditLogModel, AuthTokenLog
from .Infrastructure.user_model import UserModel
# Register your models here.
admin.site.register(AuthTokenLog)
@admin.register(AuditLogModel)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'path', 'method', 'status_code', 'city', 'country', 'device', 'browser', 'ip_address')
    list_filter = ('status_code', 'country', 'device', 'browser')
    search_fields = ('user__email', 'path', 'ip_address', 'city', 'region', 'country', 'user_agent')
    readonly_fields = [f.name for f in AuditLogModel._meta.fields]

@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password', 'is_active']

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)

