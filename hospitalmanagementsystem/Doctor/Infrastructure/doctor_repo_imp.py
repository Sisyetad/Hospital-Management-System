
from Doctor.Domain.doctor_entity import DoctorEntity
from Doctor.Domain.doctor_repo import IDoctorRepository
from Doctor.Infrastructure.doctor_model import DoctorModel
from Branch.Infrastructure.branch_model import BranchModel
from Role.Infrastructure.role_model import RoleModel
from django.core.exceptions import ValidationError

class DoctorRepository(IDoctorRepository):
    def createDoctor(self, doctor_name:str, email:str, role_model:RoleModel, department:str, phone:str, location:str, branch_model:BranchModel) -> DoctorEntity:
            doctor_model = DoctorModel.objects.create(
                doctor_name=doctor_name,
                email=email,
                role=role_model,
                phone=phone,
                location=location,
                branch=branch_model,
                department=department
            )

            return doctor_model.to_entity()

    def deleteDoctor(self, doctor_id)-> str:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")
        doctor.delete()
        return "Doctor deleted successfully."

    def getDoctor(self, doctor_id)-> DoctorEntity:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
            return doctor.to_entity()
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def getDoctorsOfBranch(self, branch_id)-> list[DoctorEntity]:
        result = DoctorModel.objects.filter(branch_id=branch_id).select_related('branch', 'role').all()
        return [doctor.to_entity() for doctor in result]

    def update(self, doctor_id, doctor_name, department)-> DoctorEntity:
        try:
            doctor = DoctorModel.objects.get(pk=doctor_id)
            doctor.doctor_name = doctor_name
            doctor.department = department
            doctor.save()
            return doctor.to_entity()
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def updateStatusofDoctor(self, status, email)-> DoctorEntity:
        try:
            doctor = DoctorModel.objects.get(email=email)
            doctor.is_available = status
            doctor.save()
            return doctor.to_entity()
        except DoctorModel.DoesNotExist:
            raise ValidationError("Doctor does not exist!")

    def getDoctors(self)-> list[DoctorEntity]:
        result = DoctorModel.objects.select_related('branch', 'role').all()
        return [doctor.to_entity() for doctor in result]
    
    def exists_by_email(self, email: str) -> bool:
        return DoctorModel.objects.filter(email=email).exists()
