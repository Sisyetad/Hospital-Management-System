from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from Role.Domain.role_entity import Role
from Admin.Domain.headoffice_entity import HeadofficeEntity
from Receptionist.Domain.receptionist_entity import ReceptionistEntity
from Doctor.Domain.doctor_entity import DoctorEntity

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
    receptionists: List[ReceptionistEntity] = field(default_factory=list)
    doctors: List[DoctorEntity] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = False
