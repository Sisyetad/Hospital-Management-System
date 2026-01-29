from django.db import models
from simple_history.models import HistoricalRecords
from encrypted_model_fields.fields import EncryptedTextField

from Diagnosis.Domain.diagnosis_entity import DiagnosisEntity
from Doctor.Infrastructure.doctor_model import DoctorModel
from Patient.Infrastructure.patient_model import PatientModel
from Branch.Infrastructure.branch_model import BranchModel


class DiagnosisModel(models.Model):
    diagnosis_name = EncryptedTextField()
    diagnosis_status = models.IntegerField(default=1)
    severity_level = models.IntegerField()
    related_symptomes = EncryptedTextField()
    clinical_notes = EncryptedTextField()
    patient = models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorModel, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='diagnosis')
    # branch = models.ForeignKey(BranchModel, 
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True)
    medication = EncryptedTextField(null=True, blank=True)
    visibility = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)    
    history = HistoricalRecords()

    def to_entity(self):
        return DiagnosisEntity(
            diagnosis_id=self.pk,
            diagnosis_name=self.diagnosis_name,
            diagnosis_status=self.diagnosis_status,
            severity_level=self.severity_level,
            related_symptomes=self.related_symptomes,
            clinical_notes=self.clinical_notes,
            patient_id=self.patient.pk,
            doctor_id=self.doctor.pk,
            medication=self.medication,
            visibility=self.visibility,
        )