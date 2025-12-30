from typing import Optional
from django.db import transaction
from Patient.Domain.patient_repo import IPatientRepository
from Patient.Infrastructure.patient_model import PatientModel
from Role.Infrastructure.role_model import RoleModel
from User.Infrastructure.user_model import UserModel
from django.core.exceptions import PermissionDenied, ValidationError
from constants.roles import ROLE_RECEPTIONIST, ROLE_PATIENT
from Receptionist.Infrastructure.receptionist_model import ReceptionistModel
from Patient.Domain.patient_entity import PatientEntity

class PatientRepository(IPatientRepository):
    def __init__(self, current_user:Optional[UserModel]):
        self.current_user = current_user

    def createPatient(self, full_name, email, phone, role_name, location, sex, birth_date)-> PatientEntity:
        if not self.current_user:
            raise PermissionDenied("Only Authenenticated user can create patient!")
        if self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("Only Receptionist can create the patient!")
        with transaction.atomic():
            receptionist = ReceptionistModel.objects.filter(email=self.current_user.email).first()
            if not receptionist:
                raise PermissionDenied("Only Receptionist can create the patient!")
            
            if PatientModel.objects.filter(email=email).exists():
                raise ValidationError("Patient with this email exists!")
            
            if role_name.lower() != ROLE_PATIENT:
                raise ValidationError("Role name is incorrect!")
            try:
                role = RoleModel.objects.get(role_name= role_name)
            except RoleModel.DoesNotExist:
                raise ValidationError(f"Role with {role_name} role name not exist!")
            
            patient = PatientModel.objects.create(
                    full_name=full_name,
                    email=email,
                    phone=phone, 
                    role=role,
                    location=location,
                    sex=sex,
                    birth_date=birth_date,
                    branch_name=receptionist.branch.branch_name
                )

            return patient.to_entity()

    def updatePatient(self, patient_id, full_name, phone, location, sex, birth_date)-> PatientEntity:
        if not self.current_user:
            raise PermissionDenied("To update user you have to authenticated!")
        if self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("You have no access to update the patient!")
        
        try:
            patient = PatientModel.objects.get(pk= patient_id)
            patient.full_name = full_name
            patient.phone = phone
            patient.location = location
            patient.sex = sex
            patient.birth_date = birth_date

            patient.save()
            return patient.to_entity()
        except PatientModel.DoesNotExist:
            raise ValidationError("Patient with this id does not exist!")

    def delelePatient(self, patient_id)-> str:
        if not self.current_user:
            raise PermissionDenied("To update user you have to authenticated!")
        if self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("You have no access to update the patient!")
        try:
            patient = PatientModel.objects.get(pk=patient_id)
            patient.delete()
            return "Patient deleted successfully."
        except PatientModel.DoesNotExist:
            raise ValidationError("Patient with this id does not exist!")
    
    def getPatientByID(self, patient_id)-> PatientEntity:
        if self.current_user is None:
            raise PermissionDenied("To get patient you have to authenticated!")
        try:
            if self.current_user.role_name.lower() == ROLE_PATIENT:
                patient = PatientModel.objects.get(email= self.current_user.email)
                return patient.to_entity()

            patient = PatientModel.objects.get(pk=patient_id)
            return patient.to_entity()
        except PatientModel.DoesNotExist:
            raise ValidationError("Patient with this id does not exist!")

    def getPatients(self)-> list[PatientEntity]:
        return [patient.to_entity() for patient in PatientModel.objects.all()]