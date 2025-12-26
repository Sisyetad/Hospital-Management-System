from abc import ABC, abstractmethod

from Branch.Infrastructure.branch_model import BranchModel
from Branch.Domain.branch_entity import BranchEntity


class IBranchRepository(ABC):
    @abstractmethod
    def createBranch(self, branch_name, email, role_name:str, speciality, phone, location)-> BranchEntity:pass

    @abstractmethod
    def deleteBranch(self, branch_id)-> str:pass

    @abstractmethod
    def updateBranch(self, branch_id, branch_name, speciality, location, phone)-> BranchEntity: pass

    @abstractmethod
    def getBranch(self, branch_id)-> BranchEntity: pass

    @abstractmethod
    def getBranches(self)-> list[BranchEntity]: pass

    @abstractmethod
    def getBranchByEmail(self, email)-> BranchEntity: pass