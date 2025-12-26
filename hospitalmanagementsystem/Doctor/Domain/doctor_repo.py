from abc import ABC, abstractmethod

from Branch.Infrastructure.branch_model import BranchModel
from Role.Infrastructure.role_model import RoleModel

from ..Domain.doctor_entity import DoctorEntity


class IDoctorRepository(ABC):

    @abstractmethod
    def createDoctor(self, doctor_name:str, email:str, role_model:RoleModel, department:str, phone:str, location:str, branch_model:BranchModel) -> DoctorEntity: pass

    @abstractmethod
    def deleteDoctor(self, doctor_id)-> str:pass

    @abstractmethod
    def getDoctor(self, doctor_id:int) -> DoctorEntity:pass

    @abstractmethod
    def getDoctorsOfBranch(self, branch_id:int) -> list[DoctorEntity]:pass

    @abstractmethod
    def update(self, doctor_id:int, doctor_name: str, department: str) -> DoctorEntity:pass

    @abstractmethod
    def updateStatusofDoctor(self, status, email)-> DoctorEntity:pass

    @abstractmethod
    def getDoctors(self) -> list[DoctorEntity]: pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool: pass