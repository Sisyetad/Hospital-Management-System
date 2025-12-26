# doctor/domain/events.py
from dataclasses import dataclass

from hospitalmanagementsystem.core.domain_event import DomainEvent

@dataclass
class DoctorCreated(DomainEvent):
    doctor_id: int
    doctor_email: str
    branch_id: int = None

@dataclass
class DoctorUpdated(DomainEvent):
    doctor_id: int
    branch_id: int = None

@dataclass
class DoctorDeleted(DomainEvent):
    doctor_id: int
    branch_id: int = None
