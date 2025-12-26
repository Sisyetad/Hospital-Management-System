from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import get_user_model
from Role.Infrastructure.role_model import RoleModel
from constants.roles import ROLE_HEADOFFICE
from Admin.Infrastructure.headoffice_model import HeadofficeModel
from decouple import config

class Command(createsuperuser.Command):
    help = 'Create a superuser with a role'

    # def add_arguments(self, parser):
    #     super().add_arguments(parser)
    #     # No additional arguments needed, as email, username, and password are handled by default

    def handle(self, *args, **options):
        UserModel = get_user_model()
        
        # Ensure ROLE_HEADOFFICE exists
        try:
            role, created = RoleModel.objects.get_or_create(role_name=ROLE_HEADOFFICE)
            if created:
                self.stdout.write(f"Created role: {ROLE_HEADOFFICE}")
        except Exception as e:
            raise CommandError(f"Error creating role: {str(e)}")

        # Get input manually
        username = config("ADMIN_USERNAME")
        email = config("ADMIN_EMAIL")
        password = config("ADMIN_PASSWORD")

        if not (username and email and password):
            raise CommandError("ADMIN_USERNAME, ADMIN_EMAIL, or ADMIN_PASSWORD not set")

        
        # while password is None:
            # password = self.get_input('Password', secret=True)
            # password2 = self.get_input('Password (again)', secret=True)
            # if password != password2:
            #     self.stderr.write("Error: Your passwords didn't match.")
            #     password = None
            #     continue
                # try:
                #     validate_password(password)
                # except DjangoValidationError as e:
                #     self.stderr.write("Error: " + "; ".join(e.messages))
                #     password = None
                # continue

        # # Validate inputs
        # if UserModel.objects.filter(email=email).exists():
        #     raise CommandError(f"Error: Email '{email}' is already taken.")
        # if UserModel.objects.filter(username=username).exists():
        #     raise CommandError(f"Error: Username '{username}' is already taken.")

        # Create superuser
        try:
            user, created = UserModel.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'password': password,  # will be hashed automatically
                    'role': role,
                    'is_superuser': True,
                    'is_staff': True,
                    'is_active': True,
                }
            )

            if not created:
                # Update password if needed
                user.set_password(password)
                user.save()
                print(f"Superuser '{email}' already exists, password updated.")

            # Create Headoffice only if not exists
            HeadofficeModel.objects.get_or_create(
                email=email,
                defaults={
                    'headoffice_name': username,
                    'role': role,
                    'is_active': True
                }
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created successfully: {email}"))
        except Exception as e:
            raise CommandError(f"Error creating superuser: {str(e)}")

    # def get_input(self, prompt, secret=False):
    #     """Helper method to get input safely."""
    #     from getpass import getpass
    #     if secret:
    #         return getpass(prompt + ': ')
    #     return input(prompt + ': ').strip()