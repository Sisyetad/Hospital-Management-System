# doctor/services/query_service.py
from typing import Optional
from Doctor.Domain.doctor_repo import IDoctorRepository
from Doctor.Domain.doctor_entity import DoctorEntity
from hospitalmanagementsystem.core.decorators import cache_get
from django.core.exceptions import ValidationError

class DoctorQueryService:
    def __init__(self, repo: IDoctorRepository):
        self.repo = repo
        
    def get_doctor(self, doctor_id) -> DoctorEntity:
        doctors = self.repo.getDoctor(doctor_id)
        if not doctors:
            raise ValidationError('There is no doctor in this hospital.')
        return doctors

    @cache_get("doctors_of_branch", "branch_id")
    def get_doctors_of_branch(self, branch_id) -> list[DoctorEntity]:
        doctors =  [doc for doc in self.repo.getDoctorsOfBranch(branch_id)]
        if not doctors:
            raise ValidationError('There is no doctor in this branch.')
        return doctors
    
    @cache_get("available_doctors", "branch_id")
    def get_available_doctors(self, branch_id) -> list[DoctorEntity]:
        doctors =  [doc for doc in self.repo.getDoctorsOfBranch(branch_id) if doc.is_available == True]
        for doc in doctors:
            print(f"Doctor: {doc.doctor_name}, is_available: {doc.is_available} (type: {type(doc.is_available)})")
        if not doctors:
            raise ValidationError('There is no available doctor in this branch.')
        return doctors
    
    @cache_get('doctors', 'all')
    def get_all_doctors(self, all=None) -> list[DoctorEntity]:
        doctors = self.repo.getDoctors()
        if not doctors:
            raise ValidationError('There are no doctors available.')
        return doctors