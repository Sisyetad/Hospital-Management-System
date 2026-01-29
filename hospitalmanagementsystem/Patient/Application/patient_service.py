from django.core.exceptions import ValidationError
from Patient.Domain.patient_repo import IPatientRepository
from Patient.Domain.patient_entity import PatientEntity
from User.Application.task import send_user_created_confirmation_email
from hospitalmanagementsystem.utility.email_verfication import is_valid_email_format


class PatientService:
    def __init__(self, repository: IPatientRepository):
        self.repository = repository

    def createPatient(self, full_name:str, email:str, phone:str, location:str, sex:str, birth_date, role_name:str)-> PatientEntity:
        try:
            if not is_valid_email_format(email):
                return ValidationError({"error": "Invalid email format"})
            patient = self.repository.createPatient(full_name=full_name, email=email, phone=phone, location=location, sex=sex, birth_date=birth_date, role_name=role_name)
            send_user_created_confirmation_email.delay(patient.email)
            return patient
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def updatePatient(self, patient_id:int, full_name:str, email:str, phone:str, location:str, sex:str, birth_date)-> PatientEntity:
        try:
            return self.repository.updatePatient(patient_id=patient_id, full_name=full_name, email=email, phone=phone, location=location, sex= sex, birth_date=birth_date)
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def deletePatient(self,patient_id:int)-> str:
        try:
            return self.repository.delelePatient(patient_id=patient_id)
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def getPatientByID(self, patient_id:int)-> PatientEntity:
        try:
            return self.repository.getPatientByID(patient_id=patient_id)
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def getPatients(self)-> list[PatientEntity]:
        try:
            return self.repository.getPatients()
        except ValidationError as e:
            raise ValidationError(str(e))