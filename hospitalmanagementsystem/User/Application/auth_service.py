from typing import Optional

from django.forms import ValidationError
from User.Domain.auth_repo import IAuthRepository
from User.Domain.user_entity import UserEntity


class AuthService:
    def __init__(self, repository: IAuthRepository):
        self.repository = repository

    def signUp(self, username: str, email: str, password: str, role_name: str, ip=None, device=None, location=None) -> UserEntity:
        try:
            return self.repository.signUp(username, email, password, role_name, ip=ip, device=device, location=location)
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def login(self, email: str, password: str, ip=None, device=None, location=None) -> Optional[UserEntity]:
        try:
            return self.repository.login(email, password, ip=ip, device=device, location=location)
        except ValidationError as e:
            raise ValidationError(str(e))
    
    def logout(self, refresh_token: str) -> None:
        try:
            self.repository.logout(refresh_token)
        except ValidationError as e:
            raise ValidationError(str(e))