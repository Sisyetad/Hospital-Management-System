from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from django.core.exceptions import ValidationError

from Role.Domain.role_entity import Role
from Branch.Domain.branch_entity import BranchEntity

@dataclass
class DoctorEntity:
    doctor_id: Optional[int]
    doctor_name: str
    email: str
    role: Role
    phone:str
    location:str
    branch: BranchEntity
    department: str
    is_active: bool
    is_available: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if '@' not in self.email:
            raise ValidationError("Invalid email format")
        # if not self.email.endswith("@hospital.org"):
        #     raise ValidationError("Doctor must have a valid @hospital.org email.")
        # if not self.phone.isdigit() or len(self.phone) != 10:
        #     raise ValidationError("Phone number must be 10 digits")