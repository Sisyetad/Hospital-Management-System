from django.db import transaction
from Doctor.Domain.doctor_entity import DoctorEntity
from Doctor.Domain.doctor_repo import IDoctorRepository
from Doctor.Infrastructure.doctor_model import DoctorModel
from Branch.Infrastructure.branch_model import BranchModel
from Role.Infrastructure.role_model import RoleModel
from django.core.exceptions import ValidationError

from Receptionist.Infrastructure.receptionist_model import ReceptionistModel

class DoctorRepository(IDoctorRepository):
    def __init__(self, current_user=None):
        # current_user is optional, but required when inferring branch from the requester
        self.current_user = current_user

    def createDoctor(self, doctor_name:str, email:str, role_name:str, department:str, phone:str, location:str, branch_email:str) -> DoctorEntity:
        try:
            role_model = RoleModel.objects.get(role_name=role_name)
        except RoleModel.DoesNotExist:
            raise ValidationError("Role does not exist!")
        try:
            if branch_email is None:
                raise ValidationError("Branch email cannot be None!")
            branch_model = BranchModel.objects.get(email=branch_email)
        except BranchModel.DoesNotExist:
            raise ValidationError("Branch does not exist!")
        
        with transaction.atomic():
            doctor_model = DoctorModel.objects.create(
                doctor_name=doctor_name,
                email=email,
                role=role_model,
                phone=phone,
                location=location,
                branch=branch_model,
                department=department
            )

            return doctor_model

    def deleteDoctor(self, doctor_id)-> str:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")
        doctor
        return "Doctor deleted successfully."

    def getDoctor(self, doctor_id)-> DoctorEntity:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
            return doctor.to_entity()
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def getDoctorsOfBranch(self, branch_id:int=None)-> list[DoctorEntity]:
        if branch_id:
            doctors = DoctorModel.objects.select_related('branch', 'role').filter(branch__id= branch_id)
        else:
            if not self.current_user:
                raise ValidationError("Current user is required to determine branch")
            if self.current_user.role.role_name.lower() == 'branch':
                doctors = BranchModel.objects.get(pk=self.current_user.professional_id).doctors.select_related('branch', 'role').all()
            elif self.current_user.role.role_name.lower() == 'doctor':
                doctors = DoctorModel.objects.select_related('branch', 'role').branch.doctors.select_related('branch', 'role').all()
            else:
                doctors = ReceptionistModel.objects.get(pk=self.current_user.professional_id).branch.doctors.select_related('branch', 'role').all()
            
        return [doctor.to_entity() for doctor in doctors]

    def getDoctorByEmail(self, email: str) -> DoctorEntity:
        try:
            doctor = DoctorModel.objects.select_related('branch', 'role').get(email=email)
            return doctor.to_entity()
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def update(self, doctor_id, doctor_name, email, department, phone, location)-> DoctorEntity:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

        if doctor_name is not None:
            doctor.doctor_name = doctor_name
        if email is not None:
            doctor.email = email
        if department is not None:
            doctor.department = department
        if phone is not None:
            doctor.phone = phone
        if location is not None:
            doctor.location = location
        doctor.save()
        return doctor

    def updateStatusofDoctor(self, email)-> DoctorModel:
        try:
            doctor = DoctorModel.objects.get(email=email)
            doctor.is_available = not doctor.is_available
            doctor.save()
            return doctor
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def getDoctors(self)-> list[DoctorEntity]:
        result = DoctorModel.objects.select_related('branch', 'role').all()
        return [doctor.to_entity() for doctor in result]
    
    def exists_by_email(self, email: str) -> bool:
        return DoctorModel.objects.filter(email=email).exists()
