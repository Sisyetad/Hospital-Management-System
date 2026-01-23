# doctor/infrastructure/event_handlers.py
from Doctor.Domain.events import DoctorCreated, DoctorUpdated, DoctorDeleted
from User.Application.task import send_user_created_confirmation_email
from hospitalmanagementsystem.core.domain_event import EventDispatcher
from hospitalmanagementsystem.core.redis_cache_helper import RedisCacheHelper

cache_helper = RedisCacheHelper()

def handle_doctor_created(event: DoctorCreated):
    cache_helper.bulk_delete([
        ('doctors_of_branch', str(event.branch_id)),
        ('available_doctors', str(event.branch_id)),
        ('doctors', 'all')
    ])
    send_user_created_confirmation_email.delay(event.doctor_email)
def handle_doctor_updated(event: DoctorUpdated):
    cache_helper.bulk_delete([
        ('doctors_of_branch', str(event.branch_id)),
        ('available_doctors', str(event.branch_id)),
        ('doctors', 'all'),
    ])

def handle_doctor_deleted(event: DoctorDeleted):
    cache_helper.bulk_delete([
        ('doctors_of_branch', str(event.branch_id)),
        ('available_doctors', str(event.branch_id)),
        ('doctors', 'all')
    ])

EventDispatcher.register(DoctorCreated, handle_doctor_created)
EventDispatcher.register(DoctorUpdated, handle_doctor_updated)
EventDispatcher.register(DoctorDeleted, handle_doctor_deleted)
