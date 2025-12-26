from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Admin.Interface.headoffice_view import HeadofficeView

router = DefaultRouter()
router.register(r'', HeadofficeView, basename='headoffice')

urlpatterns = [
    path('', include(router.urls)),
]
