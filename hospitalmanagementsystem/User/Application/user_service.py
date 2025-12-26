from typing import List

from django.forms import ValidationError
from User.Domain.user_repo import IUserRepository
from User.Domain.user_entity import UserEntity


class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def get_all_users(self) -> List[UserEntity]:
        return self.repository.get_all()


    def get_user_by_id(self, user_id: int) -> UserEntity:
        try:
            return self.repository.get_by_id(user_id)
        except ValidationError as e:
            raise ValidationError(str(e))

    def get_user_by_email(self, email: str) -> UserEntity:
        try:
            return self.repository.get_by_email(email)
        except ValidationError as e:
            raise ValidationError(str(e))

    def update_user(self, user: UserEntity) -> UserEntity:
        try:
            return self.repository.update(user)
        except ValidationError as e:
            raise ValidationError(str(e))

    def delete_user(self, user_id: int) -> None:
        try:
            self.repository.delete(user_id)
        except ValidationError as e:
            raise ValidationError(str(e))
