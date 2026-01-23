# User/Interface/serializers/custom_token_serializer.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from User.Infrastructure.user_model import UserModel
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ✅ Add custom claims here
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role.role_name
        token['is_verified'] = user.is_active
        token['professional_id'] = user.professional_id

        return token



class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs["refresh"])
        user = UserModel.objects.select_related("role").get(id=refresh["user_id"])

        access = refresh.access_token

        # 🔥 Re-add custom claims
        access["username"] = user.username
        access["email"] = user.email
        access["role"] = user.role.role_name
        access["is_verified"] = user.is_active
        access["professional_id"] = user.professional_id
        data["access_token"] = str(access)
        return data
