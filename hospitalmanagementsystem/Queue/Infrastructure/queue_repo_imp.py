from typing import Optional
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError

from Doctor.Infrastructure.doctor_model import DoctorModel
from Patient.Infrastructure.patient_model import PatientModel
from Queue.Domain.queue_repo import IQueueRepository
from Queue.Infrastructure.queue_model import QueueModel
from User.Infrastructure.user_model import UserModel
from constants.roles import ROLE_RECEPTIONIST, ROLE_DOCTOR
from Queue.Domain.queue_entity import QueueEntity


class QueueRepository(IQueueRepository):
    def __init__(self, current_user:Optional[UserModel]):
        self.current_user = current_user

    def createQueue(self, patient_id)-> QueueEntity:
        if not self.current_user:
            raise PermissionDenied("User must be Authenticated")
        if self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("This user is not allowed to create queue")
        
        try:
            patient = PatientModel.objects.get(pk=patient_id)
        except PatientModel.DoesNotExist:
            raise ValidationError("Patient with this id does not exist!")
        
        queue = QueueModel.objects.create(
            patient=patient
        )
        return queue.to_entity()
    
    def updateQueue(self, queue_id, status)-> QueueEntity:
        if not self.current_user:
            raise PermissionDenied("User must be Authenticated")
        if self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("This user is not allowed to create queue")
        
        try:
            queue = QueueModel.objects.get(pk=queue_id)
            if status == 3:
                try:
                    doctor = DoctorModel.objects.get(pk=queue.doctor.pk)
                    doctor.is_available = True
                    doctor.save()
                except DoctorModel.DoesNotExist:
                    raise ValidationError("No doctor with this id.")
            queue.status = status
            queue.save()
            return queue.to_entity()
        except QueueModel.DoesNotExist:
            raise ValidationError("Queue with this id is not found!")
    
    def deleteQueue(self, queue_id)-> str:
        try:
            queue = QueueModel.objects.get(pk=queue_id)
            if queue.status == 3:
                queue.delete()
                return "Queue deleted successfully."
            else:
                raise ValidationError("Queue is in the processing.")
        except QueueModel.DoesNotExist:
            raise ValidationError("Queue with this id is not found!")
        
    def getQueue(self, queue_id:int)-> QueueEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR and self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("Autorization is required.")
        try:
            queue = QueueModel.objects.get(pk=queue_id)
            return queue.to_entity()
        except QueueModel.DoesNotExist:
            raise ValidationError("Queue does not found.")
        
    def getQueues(self)-> list[QueueEntity]:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR and self.current_user.role_name.lower() != ROLE_RECEPTIONIST:
            raise PermissionDenied("Autorization is required.")
        
        queues = QueueModel.objects.all()
        if not queues.exists():
            return []
        return [queue.to_entity() for queue in queues]
        
    def assignPatientToDoctor(self, queue_id, doctor_id)-> QueueEntity:
        if not self.current_user:
            raise PermissionDenied("To update user you have to authenticated!")
        if (self.current_user.role_name.lower() != ROLE_RECEPTIONIST):
            raise PermissionDenied("You have no access to update the patient!")
        
        with transaction.atomic():
            try:
                queue = QueueModel.objects.get(pk=queue_id)
            except PatientModel.DoesNotExist:
                raise ValidationError("Queue does not exist with this id")
            
            try:
                doctor = DoctorModel.objects.get(pk=doctor_id, is_available=True)
                doctor.is_available = False
                doctor.save()
            except DoctorModel.DoesNotExist:
                raise ValidationError("Doctor with this id does not exist or may not available!")
            queue.doctor = doctor
            queue.save()

            return queue.to_entity()
        
    def assignPatientToDepartment(self, queue_id, department)-> QueueEntity:
        if not self.current_user:
            raise PermissionDenied("To update user you have to authenticated!")
        if (self.current_user.role_name.lower() != ROLE_RECEPTIONIST):
            raise PermissionDenied("You have no access to update the patient!")
        
        with transaction.atomic():
            available_doctors = DoctorModel.objects.filter(department=department, is_available=True)
            if not available_doctors.exists():
                raise ValidationError("No available doctors in this department.")
            selected_doctor = available_doctors.first() 
            try:
                queue = QueueModel.objects.get(pk=queue_id)
            except QueueModel.DoesNotExist:
                raise ValidationError("Queue does not exist")
        
            selected_doctor.is_available = False
            selected_doctor.save()
            queue.doctor = selected_doctor
            queue.save()
            return queue.to_entity()