from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from Receptionist.Domain.receptionist_repo import IReceptionistRepository
from User.Domain.user_entity import UserEntity
from Role.Infrastructure.role_model import RoleModel
from constants.roles import ROLE_BRANCH, ROLE_RECEPTIONIST
from Branch.Infrastructure.branch_model import BranchModel
from Receptionist.Infrastructure.receptionist_model import ReceptionistModel
from Receptionist.Domain.receptionist_entity import ReceptionistEntity


class ReceptionistRepository(IReceptionistRepository):
    def __init__(self, current_user: UserEntity):
        self.current_user = current_user

    def createReceptionist(self, receptionist_name, email, role_name:str, phone, location)-> ReceptionistEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication required!")
        
        if self.current_user.role.role_name.lower() != ROLE_BRANCH:
            raise PermissionDenied("Only Admin can create receptionist!")
        
        with transaction.atomic():
            if ReceptionistModel.objects.filter(email= email).exists():
                raise ValidationError("Receptionist with this email is alread exists!")
            
            try:
                branch = BranchModel.objects.get(email= self.current_user.email)
            except BranchModel.DoesNotExist:
                raise ValidationError("Branch does not exist!")
            if role_name.lower() != ROLE_RECEPTIONIST:
                raise ValidationError("This is not receptionist role!")
            try:
                role = RoleModel.objects.get(role_name= role_name)
            except RoleModel.DoesNotExist:
                raise ValidationError("Role does not exist!")
            
            receptionist = ReceptionistModel.objects.create(
                receptionist_name= receptionist_name,
                email= email,
                role= role,
                branch=branch,
                phone= phone,
                location= location,
                is_active= False
            )
            return receptionist.to_entity()
    
    def deleteReceptionist(self, receptionist_id)-> str:
        if not self.current_user:
            raise PermissionDenied("Authentication required!")
        
        if self.current_user.role.role_name.lower() != ROLE_BRANCH:
            raise PermissionDenied("Only Admin can delete receptionist!")
    
        try:
            receptionist = ReceptionistModel.objects.get(pk=receptionist_id)
            receptionist.delete()
            return "Receptionist deleted successfully."
        except ReceptionistModel.DoesNotExist:
            raise ValidationError("Receptionist does not exist!")
            
    def updateReceptionist(self, receptionist_id, receptionist_name, phone, location)-> ReceptionistEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is required!")
        
        if self.current_user.role.role_name.lower() != ROLE_BRANCH:
            raise PermissionDenied("Only Admin can update receptionist!")
        
        with transaction.atomic():
            try:
                receptionist = ReceptionistModel.objects.get(pk= receptionist_id)
                receptionist.receptionist_name = receptionist_name
                receptionist.phone = phone
                receptionist.location = location
                receptionist.save()
                return receptionist.to_entity()
            except ReceptionistModel.DoesNotExist:
                raise ValidationError("Receptionist does not exist!")

    def getReceptionistByID(self, receptionist_id)-> ReceptionistEntity:
        try:
            receptionist = ReceptionistModel.objects.get(pk= receptionist_id)
            return receptionist.to_entity()
        except ReceptionistModel.DoesNotExist:
            raise ValidationError("Receptionist not Found!")
        
    def getReceptionistByEmail(self, email)-> ReceptionistEntity:
        try:
            receptionist = ReceptionistModel.objects.get(email= email)
            return receptionist.to_entity()
        except ReceptionistModel.DoesNotExist:
            raise ValidationError("Receptionist not Found!")

    def getReceptionistOfBranch(self, branch_id:int=None)-> list[ReceptionistEntity]:
        if branch_id:
            receptionists = ReceptionistModel.objects.select_related('branch', 'role').filter(branch__id= branch_id)
        else:
            receptionists = ReceptionistModel.objects.select_related('branch', 'role').filter(branch__email = self.current_user.email)
        if not receptionists.exists():
            raise ValidationError("No receptionists found for this branch")
        return [receptionist.to_entity() for receptionist in receptionists]