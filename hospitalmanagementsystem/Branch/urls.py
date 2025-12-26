from rest_framework.routers import DefaultRouter
from Branch.Interface.branch_view import BranchViewSet

router = DefaultRouter()
router.register(r'', BranchViewSet, basename='branch')

urlpatterns = router.urls
