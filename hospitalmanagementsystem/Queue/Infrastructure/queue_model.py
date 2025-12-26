from django.db import models

from Doctor.Infrastructure.doctor_model import DoctorModel
from Patient.Infrastructure.patient_model import PatientModel
from Queue.Domain.queue_entity import QueueEntity

class QueueModel(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorModel, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='queues')
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def to_entity(self) -> QueueEntity:
        return QueueEntity(
            queue_id=self.pk,
            patient=self.patient,
            doctor=self.doctor,
            status=self.status,
            created_at=self.created_at,
            # updated_at=self.updated_at
        )