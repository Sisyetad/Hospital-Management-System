from django.urls import re_path
from .consumer import NotificationConsumer

websocket_urlpatterns = [
    # Pass branchId as a URL parameter
    re_path(r"api/v1/ws/notifications/$", NotificationConsumer.as_asgi()),
]
