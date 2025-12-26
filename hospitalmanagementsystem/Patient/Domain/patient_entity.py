from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from Role.Domain.role_entity import Role
from Doctor.Domain.doctor_entity import DoctorEntity


@dataclass
class PatientEntity:
    patient_id: Optional[int]
    full_name:str
    sex:str
    email: str
    phone:str
    location:str
    role: Role
    branch_name: str
    is_active: bool
    birth_date:Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None