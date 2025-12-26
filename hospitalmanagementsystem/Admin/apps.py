from django.apps import AppConfig

class AdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Admin'

    # def ready(self):
    #     from django.contrib.auth import get_user_model
    #     from django.db.utils import OperationalError
    #     from django.db import ProgrammingError
    #     from Role.Infrastructure.role_model import RoleModel
    #     from constants.roles import ROLE_HEADOFFICE
    #     from Admin.Infrastructure.headoffice_model import HeadofficeModel
    #     from decouple import config

    #     try:
    #         username = config("ADMIN_USERNAME")
    #         email = config("ADMIN_EMAIL")
    #         password = config("ADMIN_PASSWORD")

    #         if not (username and email and password):
    #             print(f"{username}, {email}, or {password} environment variables are not set.")
    #             return

    #         User = get_user_model()
    #         if User.objects.filter(username=username).exists():
    #             return

    #         role, _ = RoleModel.objects.get_or_create(role_name=ROLE_HEADOFFICE)
    #         user = User.objects.create_superuser(
    #             email=email,
    #             username=username,
    #             password=password,
    #             role=role,
    #             is_superuser=True,
    #             is_staff=True,
    #             is_active=True,
    #         )
    #         HeadofficeModel.objects.create(
    #             email=email,
    #             headoffice_name=username,
    #             role=role,
    #             is_active=True
    #         )
    #         print("✅ Superuser and HeadOffice created successfully.")
    #     except (OperationalError, ProgrammingError) as db_error:
    #         print(f"⚠️ DB not ready yet: {db_error}")
