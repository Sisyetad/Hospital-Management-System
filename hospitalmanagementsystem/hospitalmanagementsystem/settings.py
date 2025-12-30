import os
from decouple import config
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
HOST='localhost'

ALLOWED_HOSTS = [
    '*'
]

INSTALLED_APPS = [
    'corsheaders',
    'User',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'simple_history',
    # 'djoser',
    # 'django_celery_results',
    'Admin.apps.AdminConfig',
    'Role',
    'Branch',
    'Doctor',
    'Patient',
    'Receptionist',
    'Queue',
    'Diagnosis',
    'drf_spectacular',
]

AUTH_USER_MODEL = 'User.UserModel'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'hospitalmanagementsystem.core.middleware.redis_cache_middleware.RedisCacheMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ROOT_URLCONF = 'hospitalmanagementsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospitalmanagementsystem.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='5432'),
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
# ]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/minute',
        'user': '1000/day',
        'low_request': '5/minute',
        'high_request': '100/minute',
    }
}

FIELD_ENCRYPTION_KEY = config('FIELD_ENCRYPTION_KEY')

SIMPLE_HISTORY_HISTORY_USER_MODEL = 'User.UserModel'

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    "https://hospital-management-acna.onrender.com",
    "http://localhost:8000",
    "https://hospital-management-system-kappa-nine.vercel.app",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "accept",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True  # Redirect all HTTP to HTTPS.
SECURE_HSTS_SECONDS = 3600  # Enables Strict-Transport-Security.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_TRUSTED_ORIGINS = [
    f'https://{HOST}',
]
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False



SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Default
SESSION_COOKIE_NAME = 'sessionid'





# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware', # needed for `request.user`
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'simple_history.middleware.HistoryRequestMiddleware',
# ]

# if 'RUNNING_ADMIN' in os.environ:
#     MIDDLEWARE += [
#         'django.contrib.sessions.middleware.SessionMiddleware',
#         'django.middleware.csrf.CsrfViewMiddleware',
#         'django.contrib.messages.middleware.MessageMiddleware',
#     ]


SPECTACULAR_SETTINGS = {
    'TITLE': 'Medical Scheduler API',
    'DESCRIPTION': 'API for scheduling medical appointments',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # 'PARSER_CLASS': 'redis.connection.HiredisParser',
            'TIMEOUT': 60,
        },
    }
}


CELERY_BROKER_URL = config('REDIS_URL')
CELERY_RESULT_BACKEND = config('REDIS_URL')
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}


# DJOSER = {
#     'LOGIN_FIELD': 'email',
#     'USER_CREATE_PASSWORD_RETYPE': True,
#     'USER_ID_FIELD': 'id',
#     'SEND_ACTIVATION_EMAIL': True,
#     'ACTIVATION_URL': 'activate/{uid}/{token}', 
#     'SERIALIZERS': {
#         'user_create': 'User.Interface.Serializer.custom_serializer.CustomUserCreateSerializer',
#         'user': 'User.Interface.Serializer.UserSerializer',
#         'current_user': 'User.Interface.Serializer.UserSerializer',
#     },
# }

# DEFAULT_FROM_EMAIL = 'admin@medicalscheduler.com'


STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / "staticfiles"

# 
# LOGGING = {
    # 'version': 1,
    # 'disable_existing_loggers': False,
    # 'handlers': {
        # 'file': {
            # 'level': 'DEBUG',
            # 'class': 'logging.FileHandler',
            # 'filename': 'django_debug.log',
        # },
    # },
    # 'loggers': {
        # 'django': {
            # 'handlers': ['file'],
            # 'level': 'DEBUG',
            # 'propagate': True,
        # },
    # },
# }

# LOGGING = {
    # "version": 1,
    # "disable_existing_loggers": False,
    # "handlers": {
        # "console": {
            # "class": "logging.StreamHandler",
        # },
    # },
    # "root": {
        # "handlers": ["console"],
        # "level": "INFO",
    # },
# }
# 



LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

if os.environ.get("DEBUG") == "True":
    LOGGING["handlers"]["file"] = {
        "class": "logging.FileHandler",
        "filename": "django_debug.log",
    }
    LOGGING["root"]["handlers"].append("file")
