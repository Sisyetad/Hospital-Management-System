from typing import Optional
from Queue.Domain.queue_repo import IQueueRepository
from Queue.Domain.queue_entity import QueueEntity
from Doctor.Application.task import send_Patient_Assigned_notif


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
            assigned = self.repository.assignPatientToDoctor(queue_id=queue_id, doctor_id=doctor_id)
            send_Patient_Assigned_notif.apply_async(
                args=[assigned.patient.email, assigned.doctor.doctor_name],
                countdown=60  # send after 1 minute
            )
            return assigned
        except Exception as e:
            raise Exception(str(e))
        
    def assignPatientToDepartment(self, queue_id:int, department:str)-> QueueEntity:
        try:
            assigned = self.repository.assignPatientToDepartment(queue_id=queue_id, department=department)
            send_Patient_Assigned_notif.apply_async(
                args=[assigned.patient.email, assigned.doctor.doctor_name],
                countdown=60  # send after 1 minute
            )
            return assigned
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