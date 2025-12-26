from abc import ABC, abstractmethod

from Queue.Domain.queue_entity import QueueEntity


class IQueueRepository(ABC):
    @abstractmethod
    def createQueue(self, patient_id:int)-> QueueEntity:pass

    @abstractmethod
    def updateQueue(self, queue_id:int, status:int)-> QueueEntity:pass

    @abstractmethod
    def deleteQueue(self, queue_id:int)-> str:pass

    @abstractmethod
    def assignPatientToDoctor(self, queue_id:int, doctor_id:int)-> QueueEntity:pass

    @abstractmethod
    def assignPatientToDepartment(self, queue_id:int, department:str)-> QueueEntity:pass

    @abstractmethod
    def getQueue(self, queue_id:int)-> QueueEntity:pass

    @abstractmethod
    def getQueues(self)-> list[QueueEntity]:pass