from abc import ABC, abstractmethod
from ..Domain.doctor_entity import DoctorEntity


class IDoctorRepository(ABC):

    @abstractmethod
    def createDoctor(self, doctor_name:str, email:str, role_name:str, department:str, phone:str, location:str, branch_email:str) -> DoctorEntity: pass

    @abstractmethod
    def deleteDoctor(self, doctor_id)-> str:pass

    @abstractmethod
    def getDoctor(self, doctor_id:int) -> DoctorEntity:pass

    @abstractmethod
    def getDoctorsOfBranch(self, branch_id:int=None) -> list[DoctorEntity]:pass

    @abstractmethod
    def getDoctorByEmail(self, email: str) -> DoctorEntity: pass

    @abstractmethod
    def update(self, doctor_id:int, doctor_name: str, email: str, department: str, phone: str, location: str) -> DoctorEntity:pass

    @abstractmethod
    def updateStatusofDoctor(self, email)-> DoctorEntity:pass

    @abstractmethod
    def getDoctors(self) -> list[DoctorEntity]: pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool: pass