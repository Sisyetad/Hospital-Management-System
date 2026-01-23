# yourapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_Im_Available_notif(receptionists_email):
    subject = "Doctor is Available!"
    for email in receptionists_email:
        message = f"Your Doctor with email {email} is now available for consultation."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

@shared_task
def send_Patient_Assigned_notif(patient_email, doctor_name):
    subject = "Patient Assigned to Doctor!"
    message = f"Your Patient with email {patient_email} has been assigned to Doctor {doctor_name}."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email])