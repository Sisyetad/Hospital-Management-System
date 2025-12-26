from django.contrib import admin

from Patient.Infrastructure.patient_model import PatientModel

# Register your models here.
admin.site.register(PatientModel)