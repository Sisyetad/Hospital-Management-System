from typing import Optional
from User.Infrastructure.user_model import UserModel
from User.Domain.user_repo import IUserRepository
from User.Domain.user_entity import UserEntity
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class DjangoUserRepository(IUserRepository):
    def __init__(self, current_user: Optional[UserModel]):
        self.current_user = current_user

    def get_all(self)-> list[UserEntity]:
        return [user.to_entity() for user in UserModel.objects.select_related('role').all()]

    def get_by_id(self, user_id: int)-> UserEntity:
        try:
            user = UserModel.objects.select_related('role').get(pk=user_id)
            return user.to_entity()
        except UserModel.DoesNotExist:
            raise ValidationError("User does not exist!")

    def get_by_email(self, email: str)-> UserEntity:
        try:
            user = UserModel.objects.select_related('role').get(email=email)
            return user.to_entity()
        except UserModel.DoesNotExist:
            raise ValidationError("User does not exist!")

    def update(self, user: UserEntity)-> UserEntity:
        if not self.current_user:
            raise ValidationError("Authentication required!")
        try:
            user_obj = UserModel.objects.get(pk=self.current_user.id)
            user_obj.username = user.username
            user_obj.password = make_password(user.password)
            user_obj.save()
            return user_obj.to_entity()
        except UserModel.DoesNotExist:
            raise ValidationError("User does not exist!")

    def delete(self, user_id: int)-> str:
        try:
            UserModel.objects.get(pk=user_id).delete()
            return "User deleted successfully."
        except UserModel.DoesNotExist:
            raise ValidationError("User does not exist!")