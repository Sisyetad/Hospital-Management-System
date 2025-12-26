from abc import ABC, abstractmethod

from Patient.Domain.patient_entity import PatientEntity


class IPatientRepository(ABC):
    @abstractmethod
    def createPatient(self, full_name:str, email:str, phone:str, role_name:str, location:str,sex:str, birth_date)-> PatientEntity:pass

    @abstractmethod
    def updatePatient(self, patient_id:int, full_name:str, email:str, phone:str, location:str,sex:str, birth_date)-> PatientEntity:pass

    @abstractmethod
    def delelePatient(self, patient_id:int)-> str:pass

    @abstractmethod
    def getPatients(self)-> list[PatientEntity]:pass

    @abstractmethod
    def getPatientByID(self, patient_id:int)-> PatientEntity:pass