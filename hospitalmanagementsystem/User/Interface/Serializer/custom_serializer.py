# # serializers.py
# from rest_framework import serializers
# from django.db import transaction
# from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.tokens import RefreshToken

# from Admin.Infrastructure.headoffice_model import HeadofficeModel
# from Branch.Infrastructure.branch_model import BranchModel
# from Doctor.Infrastructure.doctor_model import DoctorModel
# from Patient.Infrastructure.patient_model import PatientModel
# from Receptionist.Infrastructure.receptionist_model import ReceptionistModel
# from Role.Infrastructure.role_model import RoleModel
# from User.Infrastructure.user_model import UserModel

# class CustomUserCreateSerializer(serializers.ModelSerializer):
#     role_name = serializers.CharField(write_only=True)

#     class Meta:
#         model = UserModel
#         fields = ('username', 'email', 'password', 'role_name')
#         extra_kwargs = {'password': {'write_only': True}}

#     def validate(self, attrs):
#         email = attrs['email']
#         role_name = attrs['role_name'].lower()

#         if UserModel.objects.filter(email=email).exists():
#             raise ValidationError("User with this email already exists.")

#         model_map = {
#             'headoffice': HeadofficeModel,
#             'branch': BranchModel,
#             'patient': PatientModel,
#             'doctor': DoctorModel,
#             'receptionist': ReceptionistModel
#         }

#         model = model_map.get(role_name)
#         if not model:
#             raise ValidationError("Invalid role specified.")

#         try:
#             user = model.objects.get(email=email)
#             if user.is_active:
#                 raise ValidationError("Account already activated.")
#         except model.DoesNotExist:
#             raise ValidationError(f"{role_name.title()} not found for this email.")

#         return attrs

#     def create(self, validated_data):
#         with transaction.atomic():
#             role_name = validated_data.pop('role_name')
#             email = validated_data['email']

#             role = RoleModel.objects.get(role_name__iexact=role_name)

#             # Activate role-specific model
#             model_map = {
#                 'headoffice': HeadofficeModel,
#                 'branch': BranchModel,
#                 'patient': PatientModel,
#                 'doctor': DoctorModel,
#                 'receptionist': ReceptionistModel
#             }
#             model = model_map[role_name.lower()]
#             user_role = model.objects.get(email=email)
#             user_role.is_active = True
#             user_role.save()

#             # Create main user
#             user = UserModel.objects.create(
#                 role=role,
#                 is_active=True,
#                 is_superuser=False,
#                 is_staff=False,
#                 **validated_data
#             )
#             user.set_password(validated_data['password'])
#             user.save()

#             # Generate JWT tokens
            
#             tokens = generate_tokens_for_user(user)

#             return {
#                 "user": user.to_entity(),
#                 "access_token": tokens['access'],
#                 "refresh_token": tokens['refresh']
#             }
        

# @staticmethod
# def generate_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'access': str(refresh.access_token),
#         'refresh': str(refresh)
#     }