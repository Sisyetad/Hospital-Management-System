from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from Role.Domain.role_entity import Role

@dataclass
class UserEntity:
    user_id: Optional[int]
    username: str
    email: str
    password: str
    role: Role
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None