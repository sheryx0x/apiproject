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
    "rest_framework",
    "api",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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


CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'memory://'  


# Database
# Example: for PostgreSQL set DATABASE_URL in .env: postgres://USER:PASS@HOST:PORT/NAME
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = env("STATIC_URL", default="/static/")
STATIC_ROOT = env("STATIC_ROOT", default=os.path.join(BASE_DIR, "staticfiles"))

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "api.User"

# REST framework & Simple JWT
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

# SIMPLE_JWT settings (read lifetimes from .env)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("ACCESS_TOKEN_MINUTES", default=50)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("REFRESH_TOKEN_DAYS", default=7)),
    "ALGORITHM": env("JWT_ALGORITHM", default="HS256"),
    # By default the signing key will be Django's SECRET_KEY — allow override if needed
    "SIGNING_KEY": env("JWT_SIGNING_KEY", default=SECRET_KEY),
    # add other Simple JWT settings here if you need (ROTATE_REFRESH_TOKENS, etc.)
}

# Security hardening (only applied in production)
if not DEBUG:
    # Redirect HTTP to HTTPS
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)

    # Use secure cookies
    SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=True)
    CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=True)

    # HTTP Strict Transport Security (HSTS)
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
    SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD", default=True)

    # Other security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
