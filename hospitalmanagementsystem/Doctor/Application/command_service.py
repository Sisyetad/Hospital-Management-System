# doctor/services/command_service.py
from typing import Optional
from django.core.exceptions import ValidationError
from Doctor.Domain.doctor_entity import DoctorEntity
from Doctor.Domain.doctor_repo import IDoctorRepository
from Doctor.Domain.events import DoctorCreated, DoctorUpdated, DoctorDeleted
from User.Infrastructure.user_model import UserModel
from constants.roles import ROLE_BRANCH, ROLE_DOCTOR
from Branch.Domain.branch_repo import IBranchRepository
from Role.Domain.role_repo import IRoleRepository
from User.Permission.permission import require_roles
from hospitalmanagementsystem.core.domain_event import EventDispatcher

class DoctorCommandService:
    def __init__(self, doctor_repo: IDoctorRepository, branch_repo: IBranchRepository, role_repo: IRoleRepository, current_user:Optional[UserModel]):
        self.doctor_repo = doctor_repo
        self.branch_repo = branch_repo
        self.role_repo = role_repo
        self.current_user = current_user

    @require_roles(ROLE_BRANCH)
    def create_doctor(self, doctor_name:str, email:str, role_name:str, department:str, phone:str, location:str) -> DoctorEntity:
        if self.doctor_repo.exists_by_email(email):
            raise ValidationError("A doctor with this email already exists.")

        if role_name.lower() != ROLE_DOCTOR:
            raise ValidationError('This service only to create the doctor object.')
        
        branch_model = self.branch_repo.getBranchByEmail(email=self.current_user.email)
        if not branch_model:
            raise ValidationError("Permission denied: Branch role required.")
        
        role_model = self.role_repo.getRole(role_name=role_name.lower())
        if not role_model:
            raise ValidationError("Doctor role not found.")
        
        doctor =  self.doctor_repo.createDoctor(
            doctor_name=doctor_name,
            email=email,
            role_model=role_model,
            phone=phone,
            location=location,
            branch_model=branch_model,
            department=department)
        EventDispatcher.dispatch(DoctorCreated(doctor_id=doctor.doctor_id, branch_id=branch_model.to_entity().branch_id, doctor_email=doctor.email))
        return doctor

    @require_roles(ROLE_BRANCH)
    def update_doctor(self, doctor_id, name, department) -> DoctorEntity:
        doctor = self.doctor_repo.update(doctor_id, name, department)
        if not doctor:
            raise ValidationError("Doctor update failed.")
        
        EventDispatcher.dispatch(DoctorUpdated(doctor_id=doctor.doctor_id, branch_id=doctor.branch.branch_id))
        return doctor

    @require_roles(ROLE_DOCTOR)
    def update_doctor_status(self, status)-> DoctorEntity:
        doctor = self.doctor_repo.updateStatusofDoctor(status=status, email=self.current_user.email)
        if not doctor:
            raise ValidationError("Doctor status update failed.")

        EventDispatcher.dispatch(DoctorUpdated(doctor_id=doctor.doctor_id, branch_id=doctor.branch.branch_id))
        return doctor

    @require_roles(ROLE_BRANCH)
    def delete_doctor(self, doctor_id)-> bool:
        branch_id = self.doctor_repo.getDoctor(doctor_id).branch.branch_id
        self.doctor_repo.deleteDoctor(doctor_id)
        EventDispatcher.dispatch(DoctorDeleted(doctor_id=doctor_id, branch_id=branch_id))
        return True