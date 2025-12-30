from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from User.Application.auth_service import AuthService
from User.Infrastructure.auth_repo_imp import DjangoAuthRepository
from User.Interface.Serializer.user_serializer import UserSerializer
from User.Application.token_utils import TokenUtils

from rest_framework.throttling import ScopedRateThrottle

from User.Infrastructure.user_repo_imp import DjangoUserRepository
from User.Application.user_service import UserService
from hospitalmanagementsystem.User.Domain.user_entity import UserEntity

class AuthView(APIView):
    serializer_class = UserSerializer
    service = AuthService(DjangoAuthRepository())
    
    def get_service(self, request):
        return UserService(DjangoUserRepository(request.user))
    
    throttle_scope = 'low_request'
    throttle_classes = [ScopedRateThrottle]
    
    def get_permissions(self):
        action = self.kwargs.get('action')
        if action in ['signup', 'login']:
            return [AllowAny()]
        elif action in ['logout','retrieve_profile']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_authenticators(self):
        action = self.kwargs.get('action')
        if action == 'logout':
            return [JWTAuthentication()]
        if action == 'retrieve_profile':
            return [JWTAuthentication()]
        return super().get_authenticators()
    
    def get(self, request: Request, action: str = None):
        if action == 'retrieve_profile':
            return self.retrieve_profile(request)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request, action: str = None):
        if action == 'signup':
            return self.signup(request)
        elif action == 'login':
            return self.login(request)
        elif action == 'logout':
            return self.logout(request)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

    
    def signup(self, request: Request):
        serializer = UserSerializer(data=request.data, context={'action': 'signup'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            result = self.service.signUp(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                role_name=data['role']['role_name'],
                ip=TokenUtils.get_client_ip(request),
                device=TokenUtils.get_device_info(request),
                location=TokenUtils.get_location_from_ip(TokenUtils.get_client_ip(request))
            )

            return Response({
                "access_token": result['access_token'],
                "refresh_token": result['refresh_token']
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request: Request):
        serializer = UserSerializer(data=request.data, context={'action': 'login'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = self.service.login(
                email=data.get('email'),
                password=data.get('password'),
                ip=TokenUtils.get_client_ip(request),
                device=TokenUtils.get_device_info(request),
                location=TokenUtils.get_location_from_ip(TokenUtils.get_client_ip(request))
            )
            return Response({
                "access_token": result['access_token'],
                "refresh_token": result['refresh_token']
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request: Request):
        serializer = UserSerializer(data=request.data, context={'action': 'logout'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            self.service.logout(data['refresh_token'])
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_profile(self, request):
        user = request.user
        try:
            userService = self.get_service(request)
            user = userService.get_user_by_id(user.id)
            return Response(UserSerializer(user).data, status= status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update_profile(self, request: Request):
        serializer = UserSerializer(data=request.data, context={'action': 'update_profile'})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            userService = self.get_service(request)
            user = UserEntity(
                user_id=request.user.id,
                username=data.get('username', None),
                email=data.get('email', None),
                password=data.get('password', None)
            )
            user = userService.update_user(user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)