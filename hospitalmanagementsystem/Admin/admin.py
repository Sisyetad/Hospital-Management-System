from django.contrib import admin

from Admin.Infrastructure.headoffice_model import HeadofficeModel

# Register your models here.
admin.site.register(HeadofficeModel)

from django.contrib.admin.models import LogEntry
from django.contrib import admin

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_time', 'content_type', 'object_repr', 'change_message', 'action_flag']
    readonly_fields = [f.name for f in LogEntry._meta.fields]
    ordering = ['-action_time']


from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)
