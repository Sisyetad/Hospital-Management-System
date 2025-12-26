from typing import Optional
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from simple_history.utils import update_change_reason

from Diagnosis.Domain.diagnosis_repo import IDiagnosisRepository
from Diagnosis.Infrastructure.diagnosis_model import DiagnosisModel
from Doctor.Infrastructure.doctor_model import DoctorModel
from Patient.Infrastructure.patient_model import PatientModel
from User.Infrastructure.user_model import UserModel
from constants.roles import ROLE_DOCTOR, ROLE_PATIENT, ROLE_HEADOFFICE
from Diagnosis.Domain.diagnosis_entity import DiagnosisEntity


class DiagnosisRepository(IDiagnosisRepository):
    def __init__(self, current_user:Optional[UserModel]):
        self.current_user = current_user

    def createDiagnosis(self, diagnosis_name, severity_level, related_symptomes, clinical_notes, patient_id, doctor_id, medication)-> DiagnosisEntity:
        if not self.current_user:
            raise PermissionDenied("Athentication is needed.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR:
            raise PermissionDenied("Only Doctor can create the diagnosis.")
        
        with transaction.atomic():
            try:
                patient = PatientModel.objects.get(pk=patient_id)
            except PatientModel.DoesNotExist:
                raise ValidationError("Patient with this id is not found.")
            
            try:
                doctor = DoctorModel.objects.get(pk=doctor_id)
            except DoctorModel.DoesNotExist:
                raise ValidationError("Doctor with this id is not found.")
            
            diagnosis = DiagnosisModel.objects.create(
                diagnosis_name=diagnosis_name,
                severity_level=severity_level,
                related_symptomes=related_symptomes,
                clinical_notes=clinical_notes,
                patient=patient,
                doctor=doctor,
                medication=medication,
                visibility=True
            )
            return diagnosis.to_entity()

    def updateDiagnosis(self, diagnosis_id, severity_level, related_symptomes, clinical_notes, doctor_id, medication, updation_reason)-> DiagnosisEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is needed.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR:
            raise PermissionDenied("Only Doctor can update the diagnosis.")

        with transaction.atomic():
            try:
                diagnosis = DiagnosisModel.objects.get(pk=diagnosis_id)
            except DiagnosisModel.DoesNotExist:
                raise ValidationError("Diagnosis with this ID is not found.")

            try:
                doctor = DoctorModel.objects.get(pk=doctor_id)
            except DoctorModel.DoesNotExist:
                raise ValidationError("Doctor with this ID is not found.")
            diagnosis.diagnosis_name = diagnosis.diagnosis_name
            diagnosis.severity_level = severity_level
            diagnosis.related_symptomes = related_symptomes
            diagnosis.clinical_notes = clinical_notes
            diagnosis.doctor = doctor
            diagnosis.medication = medication

            diagnosis._history_user = self.current_user
            diagnosis._history_change_reason = updation_reason or "Updated diagnosis"

            diagnosis.save()

            return diagnosis.to_entity()

    def getDiagnoses(self,  patient_id)-> list[DiagnosisEntity]:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")
        if self.current_user.role_name.lower() != ROLE_PATIENT:
            diagnoses = DiagnosisModel.objects.filter(
                patient__pk=patient_id,
                visibility=True
            )
            if not diagnoses.exists():
                raise ValidationError("No diagnosis found.")
        else:
            diagnoses = DiagnosisModel.objects.filter(patient__email=self.current_user.email)
            if not diagnoses.exists():
                raise ValidationError("No diagnosis found.")

        return [diagnosis.to_entity() for diagnosis in diagnoses]
    
    def getDiagnosis(self, diagnosis_id)-> DiagnosisEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR and self.current_user.role_name.lower() != ROLE_PATIENT:
            raise PermissionDenied("Permission is denied.")
        try:
            diagnosis = DiagnosisModel.objects.get(pk=diagnosis_id)
            if not diagnosis.visibility and self.current_user.role_name.lower() != ROLE_PATIENT:
                raise PermissionDenied("This diagnosis is hidden by the patient.")
            return diagnosis.to_entity()

        except DiagnosisModel.DoesNotExist:
            raise ValidationError("Diagnosis does not found.")
    
    def verify_vissiblity(self, diagnosis_id)-> DiagnosisEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")
        if self.current_user.role_name.lower() != ROLE_PATIENT:
            raise PermissionDenied("Only the patient can change visibility settings.")

        try:
            diagnosis = DiagnosisModel.objects.get(pk=diagnosis_id)
        except DiagnosisModel.DoesNotExist:
            raise ValidationError("Diagnosis not found.")

        if diagnosis.patient.email != self.current_user.email:
            raise PermissionDenied("You cannot change visibility of others' diagnoses.")

        diagnosis.visibility = not diagnosis.visibility
        diagnosis.save()
        return diagnosis.to_entity()
    
    def displayHistory(self, diagnosis_id)-> list[dict]:
        if not self.current_user:
            raise PermissionDenied("Authentication is required.")

        if self.current_user.role_name.strip().lower() != ROLE_HEADOFFICE:
            raise PermissionDenied("Only the headoffice can display history version.")

        try:
            diagnosis = DiagnosisModel.objects.get(pk=diagnosis_id)
        except DiagnosisModel.DoesNotExist:
            raise ValidationError("Diagnosis not found.")

        history_queryset = diagnosis.history.all().order_by('-history_date')  # Optional: latest first

        history_list = []
        for record in history_queryset:
            history_list.append({
                'diagnosis_name': record.diagnosis_name,
                'diagnosis_status': record.diagnosis_status,
                'severity_level': record.severity_level,
                'related_symptomes': record.related_symptomes,
                'clinical_notes': record.clinical_notes,
                'medication': record.medication,
                'visibility': record.visibility,
                'modified_by': str(record.history_user) if record.history_user else None,
                'change_reason': record.history_change_reason,
                'history_date': record.history_date,
                'history_type': record.get_history_type_display(),
            })

        return history_list


    def updateDiagnosisStatus(self, diagnosis_id, diagnosis_status)-> DiagnosisEntity:
        if not self.current_user:
            raise PermissionDenied("Authentication is needed.")
        if self.current_user.role_name.lower() != ROLE_DOCTOR:
            raise PermissionDenied("Only Doctor can update the diagnosis.")

        try:
            diagnosis = DiagnosisModel.objects.get(pk=diagnosis_id)
        except DiagnosisModel.DoesNotExist:
            raise ValidationError("Diagnosis with this ID is not found.")
        diagnosis.diagnosis_status=diagnosis_status
        diagnosis.save()
        return diagnosis.to_entity()