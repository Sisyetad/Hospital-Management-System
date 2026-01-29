from django.forms import ValidationError
from Receptionist.Domain.receptionist_repo import IReceptionistRepository
from Receptionist.Domain.receptionist_entity import ReceptionistEntity
from User.Application.task import send_user_created_confirmation_email
from hospitalmanagementsystem.utility.email_verfication import is_valid_email_format


class ReceptionistService:
    def __init__(self, repository: IReceptionistRepository):
        self.repository= repository

    def createReceptionist(self, receptionist_name, email, phone, role_name, location)-> ReceptionistEntity:
        try:
            if not is_valid_email_format(email):
                return ValidationError({"error": "Invalid email format"})
            rec = self.repository.createReceptionist(receptionist_name=receptionist_name, email=email, phone=phone, role_name=role_name, location=location)
            send_user_created_confirmation_email.delay(rec.email)
            return rec
        except ValidationError as e:
            raise ValidationError(str(e))

    def deleteReceptionist(self, receptionist_id)-> bool:
        try:
            return self.repository.deleteReceptionist(receptionist_id=receptionist_id)
        except ValidationError as e:
            raise ValidationError(str(e))

    def updateReceptionist(self, receptionist_id, receptionist_name, phone, location)-> ReceptionistEntity:
        try:
            return self.repository.updateReceptionist(receptionist_id=receptionist_id, receptionist_name=receptionist_name, phone=phone, location=location)
        except ValidationError as e:
            raise ValidationError(str(e))

    def getReceptionistByID(self, receptionist_id)-> ReceptionistEntity:
        try:
            return self.repository.getReceptionistByID(receptionist_id=receptionist_id)
        except ValidationError as e:
            raise ValidationError(str(e))
        
    def getReceptionistByEmail(self, email)-> ReceptionistEntity:
        try:
            return self.repository.getReceptionistByEmail(email=email)
        except ValidationError as e:
            raise ValidationError(str(e))

    def getReceptionistOfBranch(self, branch_id:int=None)-> list[ReceptionistEntity]:
        try:
            return self.repository.getReceptionistOfBranch(branch_id=branch_id)
        except ValidationError as e:
            raise ValidationError(str(e))