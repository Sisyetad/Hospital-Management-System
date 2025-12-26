from .Interface.doctor_view import DoctorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DoctorViewSet, basename= 'doctor')

urlpatterns= router.urls