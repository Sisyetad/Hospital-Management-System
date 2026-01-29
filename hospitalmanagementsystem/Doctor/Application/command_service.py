# doctor/services/command_service.py
from django.core.exceptions import ValidationError
from Doctor.Domain.doctor_entity import DoctorEntity
from Doctor.Domain.doctor_repo import IDoctorRepository
from Doctor.Domain.events import DoctorCreated, DoctorUpdated, DoctorDeleted
from constants.roles import ROLE_BRANCH, ROLE_DOCTOR
from Branch.Domain.branch_repo import IBranchRepository
from Role.Domain.role_repo import IRoleRepository
from User.Permission.permission import require_roles
from Doctor.Application.task import send_Im_Available_notif
from hospitalmanagementsystem.core.domain_event import EventDispatcher
from hospitalmanagementsystem.utility.email_verfication import is_valid_email_format

class DoctorCommandService:
    def __init__(self, doctor_repo: IDoctorRepository, branch_repo: IBranchRepository, role_repo: IRoleRepository, current_user=None):
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
        if not is_valid_email_format(email):
            return ValidationError({"error": "Invalid email format"})
        doctor =  self.doctor_repo.createDoctor(
            doctor_name=doctor_name,
            email=email,
            role_name=role_name,
            phone=phone,
            location=location,
            department=department,
            branch_email=self.current_user.email)
        EventDispatcher.dispatch(DoctorCreated(doctor_id=doctor.pk, branch_id=doctor.branch.pk, doctor_email=doctor.email))
        return doctor.to_entity()

    @require_roles(ROLE_BRANCH)
    def update_doctor(self, doctor_id, doctor_name=None, email=None, department=None, phone=None, location=None) -> DoctorEntity:
        if not any([doctor_name, department, email, phone, location]):
            raise ValidationError("At least one field must be provided for update.")

        doctor = self.doctor_repo.update(
            doctor_id=doctor_id,
            doctor_name=doctor_name,
            email=email,
            department=department,
            phone=phone,
            location=location,
        )

        if not doctor:
            raise ValidationError("Doctor update failed.")
        
        EventDispatcher.dispatch(DoctorUpdated(doctor_id=doctor.pk, branch_id=doctor.branch.pk))
        return doctor.to_entity()

    @require_roles(ROLE_DOCTOR)
    def update_doctor_status(self)-> DoctorEntity:
        doctor = self.doctor_repo.updateStatusofDoctor(email=self.current_user.email)
        if not doctor:
            raise ValidationError("Doctor status update failed.")
        if doctor.is_available:
            send_Im_Available_notif.apply_async(args=[[r.email for r in doctor.branch.receptionists.all()], doctor.branch.pk, doctor.doctor_name])
        EventDispatcher.dispatch(DoctorUpdated(doctor_id=doctor.pk, branch_id=doctor.branch.pk))
        return doctor.to_entity()

    @require_roles(ROLE_BRANCH)
    def delete_doctor(self, doctor_id)-> bool:
        branch_id = self.doctor_repo.getDoctor(doctor_id).branch.branch_id
        self.doctor_repo.deleteDoctor(doctor_id)
        EventDispatcher.dispatch(DoctorDeleted(doctor_id=doctor_id, branch_id=branch_id))
        return True