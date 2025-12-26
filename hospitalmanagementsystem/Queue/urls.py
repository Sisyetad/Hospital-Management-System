from rest_framework.routers import DefaultRouter

from Queue.Interface.queue_view import QueueViewSet


router = DefaultRouter()
router.register(r'', QueueViewSet, basename= 'queue')

urlpatterns = router.urls
