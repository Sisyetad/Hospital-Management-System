from typing import Optional
from User.Infrastructure.user_model import UserModel
from Branch.Domain.branch_entity import BranchEntity
from ..Domain.branch_repo import IBranchRepository
from django.core.exceptions import ValidationError
from ..Domain.branch_repo import IBranchRepository
from django.core.exceptions import PermissionDenied
from constants.roles import ROLE_HEADOFFICE, ROLE_BRANCH

class BranchService:
    def __init__(self, current_user:Optional[UserModel],repository: IBranchRepository):
        self.repository = repository
        self.current_user = current_user

    def createBranch(self, branch_name, email, role_name:str, speciality, phone, location)-> BranchEntity:
                # Check if user is authenticated
        if not self.current_user or not hasattr(self.current_user, 'is_authenticated') or not self.current_user.is_authenticated:
            raise PermissionDenied(f"Current user: {self.current_user}")
        
        # Check if user has a role assigned
        if not hasattr(self.current_user, 'role') or self.current_user.role is None:
            raise PermissionDenied(f"Current user: {self.current_user}")

        # Check role permission
        if self.current_user.role.role_name.lower() != ROLE_HEADOFFICE.lower():
            raise PermissionDenied("Only admins can create Branch.")

        if role_name.lower() != ROLE_BRANCH:
            raise ValidationError("This is not the branch role name")
        
        try:
            return self.repository.createBranch(branch_name, email, role_name, speciality, phone, location)
        except ValidationError as e:
            raise ValidationError(str(e))

    def deleteBranch(self, branch_id)-> str:
        try:
            return self.repository.deleteBranch(branch_id)
        except ValidationError as e:
            raise ValidationError(str(e))

    def updateBranch(self, branch_id, branch_name, speciality, location, phone)-> BranchEntity:
        try:
            return self.repository.updateBranch(branch_id, branch_name, speciality, location, phone)
        except ValidationError as e:
            raise ValidationError(str(e))

    def getBranch(self, branch_id)-> BranchEntity:
        try:
            return self.repository.getBranch(branch_id=branch_id)
        except ValidationError as e:
            raise ValidationError(str(e))

    def getBranches(self)-> list[BranchEntity]:
        try:
            return self.repository.getBranches()
        except ValidationError as e:
            raise ValidationError(str(e))