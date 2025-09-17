"""
Django settings for school_project project.

Converted to use django-environ for environment configuration.
"""
import environ
import os
from pathlib import Path
from datetime import timedelta

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialise environment
env = environ.Env(
    # casting and defaults (can still be overridden in .env)
    DEBUG=(bool, False),
    ACCESS_TOKEN_MINUTES=(int, 50),
    REFRESH_TOKEN_DAYS=(int, 7),
    USER_THROTTLE_RATE=(str, "10/minute"),
)

# Read .env file (BASE_DIR/.env)
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

# Application definition
INSTALLED_APPS = [
    # built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third-party
    "silk",
    "django_celery_beat",
    "rest_framework",

    # local apps
    "api",
]

# Middleware: Silk must be first so it can intercept requests correctly.
MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",                      # Silk profiling
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",           # add WhiteNoise for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "api.middleware.BlockPUTRequestsMiddleware",
]

ROOT_URLCONF = "school_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # add template dirs or keep empty
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "school_project.wsgi.application"

# Celery (development/testing convenience)
# NOTE: set to False in production
CELERY_TASK_ALWAYS_EAGER = True

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# Database
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = env("STATIC_ROOT", default=os.path.join(BASE_DIR, "staticfiles"))
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "api.User"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": env("USER_THROTTLE_RATE", default="10/minute"),
    },
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("ACCESS_TOKEN_MINUTES", default=50)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("REFRESH_TOKEN_DAYS", default=7)),
    "ALGORITHM": env("JWT_ALGORITHM", default="HS256"),
    "SIGNING_KEY": env("JWT_SIGNING_KEY", default=SECRET_KEY),
}

# Security hardening (only applied in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

# Silk settings

from api.silk_utils import silk_intercept
SILKY_INTERCEPT_FUNC = silk_intercept   
SILKY_PYTHON_PROFILER = True
SILKY_META = True

SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = -1

SILKY_AUTHENTICATION = False
SILKY_AUTHORISATION = False

