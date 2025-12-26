from rest_framework.routers import DefaultRouter
from .Interface.receptionist_view import ReceptionistViewSet

router = DefaultRouter()
router.register(r'', ReceptionistViewSet, basename= 'receptionist')

urlpatterns= router.urls