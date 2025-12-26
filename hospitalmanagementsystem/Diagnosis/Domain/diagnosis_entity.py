from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from Doctor.Domain.doctor_entity import DoctorEntity
from Patient.Domain.patient_entity import PatientEntity

@dataclass
class DiagnosisEntity:
    diagnosis_id: int
    diagnosis_name:str
    diagnosis_status:str
    severity_level:str
    related_symptomes:str
    clinical_notes:str
    patient_id:int
    doctor_id:int
    medication:str
    visibility:bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
