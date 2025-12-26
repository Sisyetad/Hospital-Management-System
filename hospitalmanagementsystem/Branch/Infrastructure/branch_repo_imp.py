from typing import Optional
from django.core.exceptions import ValidationError

from Branch.Domain.branch_entity import BranchEntity
from .branch_model import BranchModel
from Role.Infrastructure.role_model import RoleModel
from User.Infrastructure.user_model import UserModel
from Admin.Infrastructure.headoffice_model import HeadofficeModel
from ..Domain.branch_repo import IBranchRepository

class BranchRepository(IBranchRepository):
    def __init__(self, current_user: Optional[UserModel]):
        self.current_user = current_user

    def createBranch(self, branch_name, email, role_name:str, speciality, phone, location)-> BranchEntity:

        try:
            role = RoleModel.objects.get(role_name=role_name)
        except RoleModel.DoesNotExist:
            raise ValidationError("Invalid role name!")

        if BranchModel.objects.filter(email=email).exists():
            raise ValidationError("Branch with this email already exists.")

        try:
            headoffice = HeadofficeModel.objects.get(email=self.current_user.email)
        except HeadofficeModel.DoesNotExist:
            raise ValidationError("Invalid headoffice")

        branch = BranchModel.objects.create(
            branch_name=branch_name,
            email=email,
            role=role,
            speciality=speciality,
            phone=phone,
            location=location,
            headoffice=headoffice
        )

        return branch.to_entity()

    def deleteBranch(self, branch_id)-> str:
        try:
            branch = BranchModel.objects.get(pk=branch_id)
            branch.delete()
            return "Branch deleted successfully."
        except BranchModel.DoesNotExist:
            raise ValidationError("Branch does not exist!")

    def updateBranch(self, branch_id, branch_name, speciality, location, phone)-> BranchEntity:
        try:
            branch = BranchModel.objects.get(pk=branch_id)
            branch.branch_name = branch_name
            branch.speciality = speciality
            branch.location = location
            branch.phone = phone
            branch.save()
            return branch.to_entity()
        except BranchModel.DoesNotExist:
            raise ValidationError("Branch does not exist!")

    def getBranch(self, branch_id)-> BranchEntity:
        try:
            branch = BranchModel.objects.get(pk=branch_id)
            return branch.to_entity()
        except BranchModel.DoesNotExist:
            raise ValidationError("Branch does not exist!")

    def getBranches(self)-> list[BranchEntity]:
        return [branch.to_entity() for branch in BranchModel.objects.select_related('headoffice').all()]

    def getBranchByEmail(self, email)-> BranchEntity:
        try:
            branch = BranchModel.objects.get(email=email)
            return branch.to_entity()
        except BranchModel.DoesNotExist:
            raise ValidationError("Branch with this email does not exist.")