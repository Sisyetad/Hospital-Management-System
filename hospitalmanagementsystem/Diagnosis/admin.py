from django.contrib import admin

from django.contrib import admin
from .models import DiagnosisModel

@admin.register(DiagnosisModel)
class DiagnosisAdmin(admin.ModelAdmin):
    exclude = ['medication', 'diagnosis_name', 'related_symptomes', 'clinical_notes']

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)

    def has_view_permission(self, request, obj=None):
        return super().has_view_permission(request, obj)
