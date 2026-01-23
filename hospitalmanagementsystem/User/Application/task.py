from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_user_created_confirmation_email(user_email):
    subject = "User is created!"
    message = f"You can signup now your User Email {user_email} is already created."
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])