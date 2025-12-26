from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from Doctor.Domain.doctor_entity import DoctorEntity
from Patient.Domain.patient_entity import PatientEntity


@dataclass
class QueueEntity:
    queue_id: int
    patient:PatientEntity
    doctor:DoctorEntity
    status:int
    created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None