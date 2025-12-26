# yourapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_doctor_created_confirmation_email(doctor_id, user_email):
    subject = "Doctor is created!"
    message = f"You can signup now you doctor Id {doctor_id} is already created."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])