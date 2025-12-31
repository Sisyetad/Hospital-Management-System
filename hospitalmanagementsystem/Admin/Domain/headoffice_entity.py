from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from Role.Domain.role_entity import Role
from User.Domain.user_entity import UserEntity


@dataclass
class HeadofficeEntity:
    headoffice_id: Optional[int]
    user: Optional[UserEntity]
    headoffice_name: str
    email: str
    role: Role
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    is_active: bool