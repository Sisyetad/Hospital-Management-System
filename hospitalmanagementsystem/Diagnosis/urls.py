from rest_framework.routers import DefaultRouter

from Diagnosis.Interface.diagnosis_view import DiagnosisViewSet

roter = DefaultRouter()
roter.register(r'', DiagnosisViewSet, basename='diagnosis')

urlpatterns=roter.urls