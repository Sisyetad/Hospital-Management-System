# medicalschedulerbackend/celery.py

import os
import ssl
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hospitalmanagementsystem.settings")

broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_REQUIRED
}

redis_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_REQUIRED
}

celery_app = Celery("hospitalmanagementsystem")

# Celery settings
celery_app.conf.update(
    broker_use_ssl=broker_use_ssl,
    redis_backend_use_ssl=redis_backend_use_ssl,
)
# Load config from Django settings using namespace CELERY_
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks inside all apps
celery_app.autodiscover_tasks()
