from typing import Optional
from Queue.Domain.queue_repo import IQueueRepository
from Queue.Domain.queue_entity import QueueEntity


class QueueService:
    def __init__(self, repository:IQueueRepository):
        self.repository = repository

    def createQueue(self, patient_int:int)-> QueueEntity:
        try:
            return self.repository.createQueue(patient_id=patient_int)
        except Exception as e:
            raise Exception(str(e))
        
    def updateQueue(self, queue_id:int, status:int)-> Optional[QueueEntity]:
        try:
            return self.repository.updateQueue(queue_id=queue_id, status=status)
        except Exception as e:
            raise Exception(str(e))
        
    def deleteQueue(self, queue_id:int)-> str:
        try:
            return self.repository.deleteQueue(queue_id=queue_id)
        except Exception as e:
            raise Exception(str(e))
        
    def assignPatientToDoctor(self, queue_id:int, doctor_id:int)-> QueueEntity:
        try:
            return self.repository.assignPatientToDoctor(queue_id=queue_id, doctor_id=doctor_id)
        except Exception as e:
            raise Exception(str(e))
        
    def assignPatientToDepartment(self, queue_id:int, department:str)-> QueueEntity:
        try:
            return self.repository.assignPatientToDepartment(queue_id=queue_id, department=department)
        except Exception as e:
            raise Exception(str(e))
        
    def getQueue(self, queue_id:int)-> QueueEntity:
        try:
            return self.repository.getQueue(queue_id=queue_id)
        except Exception as e:
            raise Exception(str(e))
        
    def getQueues(self)-> list[QueueEntity]:
        try:
            return self.repository.getQueues()
        except Exception as e:
            raise Exception(str(e))