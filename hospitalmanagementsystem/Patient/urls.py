from django.urls import path
from rest_framework.routers import DefaultRouter

from Patient.Interface.patient_view import PatientViewSet
from Diagnosis.Interface.diagnosis_view import DiagnosisViewSet

router = DefaultRouter()
router.register(r'', PatientViewSet, basename= 'patient')
# Export router urls so Django can populate patterns correctly
urlpatterns = router.urls
