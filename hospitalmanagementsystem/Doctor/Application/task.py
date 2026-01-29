# yourapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_Im_Available_notif(self, receptionists_email, branch_id):
    subject = "Doctor is Available!"
    channel_layer = get_channel_layer()  # Get the channel layer for WebSocket
    
    for email in receptionists_email:
        message = f"Your Doctor with email {email} is now available for consultation."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        
    async_to_sync(channel_layer.group_send)(
        "receptionists",  # Group name that receptionist clients subscribe to
        {
            "type": "send_notification",  # Handler method in consumer
            "message": message,
        }
    )

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_Patient_Assigned_notif(self, patient_email, doctor_name):
    subject = "Patient Assigned to Doctor!"
    message = f"Your Patient with email {patient_email} has been assigned to Doctor {doctor_name}."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [patient_email], 
                    fail_silently=False)