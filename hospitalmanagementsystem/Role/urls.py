from rest_framework.routers import DefaultRouter
from .Interface.role_view import RoleView

router = DefaultRouter()
router.register(r'', RoleView, basename='role')
urlpatterns = router.urls