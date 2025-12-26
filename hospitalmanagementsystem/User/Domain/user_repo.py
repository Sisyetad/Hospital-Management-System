from abc import ABC, abstractmethod
from typing import List
from User.Domain.user_entity import UserEntity

class IUserRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[UserEntity]: pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> UserEntity: pass

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity: pass

    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity: pass

    @abstractmethod
    def delete(self, user_id: int) -> None: pass