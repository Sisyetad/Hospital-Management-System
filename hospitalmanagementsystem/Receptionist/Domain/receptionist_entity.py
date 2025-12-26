from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from Role.Domain.role_entity import Role

@dataclass
class ReceptionistEntity:
    receptionist_id: Optional[int]
    receptionist_name: str
    email: str
    phone: str
    location: str
    branch: str
    role: Role
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = False