from abc import ABC, abstractmethod

from Diagnosis.Domain.diagnosis_entity import DiagnosisEntity


class IDiagnosisRepository(ABC):
    @abstractmethod
    def createDiagnosis(self, diagnosis_name:str, severity_level:int, related_symptomes:str, clinical_notes:str, patient_id:int, medication:str)-> DiagnosisEntity:pass

    @abstractmethod
    def updateDiagnosis(self, diagnosis_id:int, severity_level:str, related_symptomes:str, clinical_notes:str, medication:str, updation_reason:str)-> DiagnosisEntity:pass

    @abstractmethod
    def getDiagnosis(self, diagnosis_id:int)-> DiagnosisEntity:pass

    @abstractmethod
    def getDiagnoses(self, patient_id)-> list[DiagnosisEntity]:pass

    @abstractmethod
    def verify_vissiblity(self, diagnosis_id:int)-> DiagnosisEntity:pass

    @abstractmethod
    def displayHistory(self, diagnosis_id)-> list[dict]:pass

    @abstractmethod
    def updateDiagnosisStatus(self, diagnosis_id, diagnosis_status)-> DiagnosisEntity:pass