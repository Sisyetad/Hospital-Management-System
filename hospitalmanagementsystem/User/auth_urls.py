# medicalschedullerbackend/User/urls.py

from django.urls import path
from .Interface.View.auth_view import AuthView
from rest_framework_simplejwt.views import TokenRefreshView

from User.Interface.Serializer.token_serializer import CustomTokenRefreshSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


urlpatterns = [
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('<str:action>/', AuthView.as_view(), name='auth-action')
]