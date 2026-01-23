from typing import Dict
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from datetime import timezone
from django.core.exceptions import ValidationError
from Role.Infrastructure.role_model import RoleModel
from User.Domain.auth_repo import IAuthRepository
from User.Infrastructure.user_model import UserModel
from Doctor.Infrastructure.doctor_model import DoctorModel
from Branch.Infrastructure.branch_model import BranchModel
from Patient.Infrastructure.patient_model import PatientModel
from Receptionist.Infrastructure.receptionist_model import ReceptionistModel
from User.Infrastructure.token_model import AuthTokenLog
from constants.roles import ROLE_BRANCH, ROLE_DOCTOR, ROLE_HEADOFFICE, ROLE_PATIENT, ROLE_RECEPTIONIST
from Admin.Infrastructure.headoffice_model import HeadofficeModel
from User.Interface.Serializer.token_serializer import CustomTokenObtainPairSerializer

class DjangoAuthRepository(IAuthRepository):
    def signUp(self, username: str, email: str, password: str, role_name: str, ip, device, location) -> Dict:
        with transaction.atomic():
            try:
                # Validate role
                role = RoleModel.objects.get(role_name = role_name)
            except RoleModel.DoesNotExist:
                raise ValidationError("Invalid role ID.")

            # Check if UserModel already exists
            if UserModel.objects.filter(email=email).exists():
                raise ValidationError("User with this email already exists.")

            # Role-specific validation
            role_name = role.role_name.lower()
            if role_name == ROLE_HEADOFFICE:
                model = HeadofficeModel 
            elif role_name == ROLE_BRANCH:
                model = BranchModel
            elif role_name == ROLE_PATIENT:
                model = PatientModel
            elif role_name == ROLE_DOCTOR:
                model = DoctorModel
            elif role_name == ROLE_RECEPTIONIST:
                model = ReceptionistModel
            else:
                raise ValidationError("Invalid role specified.")

            # Validate role-specific model
            try:
                user = model.objects.get(email=email)
                if user.is_active:
                    raise ValidationError("Account already activated.")
            except model.DoesNotExist:
                raise ValidationError(f"{role_name.title()} not found for this email.")

            # Update role-specific model
            user.is_active = True
            user.save()

            # Create UserModel
            user_model = UserModel(
                username=username,
                email=email,
                professional_id=user.pk,
                role=role,
                is_active=True,
                is_superuser=False,
                is_staff=False
            )
            user_model.set_password(password)  # Hash the password
            user_model.save()

            # Generate and store tokens
            tokens = self.generate_tokens_for_user(user_model)
            AuthTokenLog.objects.create(
                user=user_model,
                refresh_token=tokens["refresh"],
                is_active=True,
                ip_address=ip,
                device=device,
                location=location
            )


            return {
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"]
            }

    def login(self, email: str, password: str, ip, device, location) -> Dict:
        with transaction.atomic():
            try:
                user = UserModel.objects.select_related('role').get(email=email)
                if not user.is_active:
                    raise ValidationError("Account not activated.")
                if not check_password(password, user.password):
                    raise ValidationError("Incorrect password.")

                # Invalidate old tokens
                AuthTokenLog.objects.filter(user=user, is_active=True).update(is_active=False)

                # Generate and store new tokens
                tokens = self.generate_tokens_for_user(user)
                AuthTokenLog.objects.create(
                    user=user,
                    refresh_token=tokens["refresh"],
                    is_active=True,
                    ip_address=ip,
                    device=device,
                    location=location
                )

                return {
                    "access_token": tokens["access"],
                    "refresh_token": tokens["refresh"]
                }
            except UserModel.DoesNotExist:
                raise ValidationError("User with this email does not exist.")
            

    def logout(self, refresh_token: str) -> None:
        if not self.use_token_model:
            raise ValidationError("Logout not supported without token storage.")
        if token.expired_at < timezone.now():
            raise ValidationError("Token already expired.")

        try:
            token = AuthTokenLog.objects.get(refresh_token=refresh_token, is_active=True)
            token.is_active = False
            token.save()
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except AuthTokenLog.DoesNotExist:
            raise ValidationError("Invalid or inactive refresh token.")

    @staticmethod
    def generate_tokens_for_user(user: UserModel) -> Dict[str, str]:
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        # active_tokens = AuthTokenLog.objects.filter(user=user, is_active=True)
        # if active_tokens.count() >= 3:
        #     oldest_token = active_tokens.order_by("expired_at").first()
        #     oldest_token.is_active = False
        #     oldest_token.save()
        # return {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token),
        # }
    
    # def get_profile(self, access_token: str) -> UserModel:
        # try:
            # user_email = CustomTokenObtainPairSerializer().get_token(access_token)['email']
            # user = UserModel.objects.select_related('role').get(email=user_email)
            # return user
        # except UserModel.DoesNotExist:
            # raise ValidationError("User does not exist.")