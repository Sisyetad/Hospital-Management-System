from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from Role.Domain.role_entity import Role
from Admin.Domain.headoffice_entity import HeadofficeEntity

@dataclass
class BranchEntity:
    branch_id: Optional[int]
    branch_name: str
    email: str
    speciality: str
    role: Role
    headoffice: HeadofficeEntity
    phone: str = '+251'
    location: str = 'online'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = False
