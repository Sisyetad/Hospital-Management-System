
from User.Interface.View.user_view import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', UserViewSet, basename= 'user')

urlpatterns = router.urls
