"""
Django settings for config project.
"""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)

from decouple import config
from urllib.parse import urlparse, parse_qsl

BASE_DIR = Path(__file__).resolve().parent.parent


# -------------------
# SECURITY
# -------------------
SECRET_KEY = config("SECRET_KEY", default="django-insecure-default-key")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=lambda v: v.split(","))


# -------------------
# DATABASE (NEON SAFE)
# -------------------
DATABASE_URL = config("DATABASE_URL")

tmpPostgres = urlparse(DATABASE_URL)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": tmpPostgres.path.lstrip("/"),
        "USER": tmpPostgres.username,
        "PASSWORD": tmpPostgres.password,
        "HOST": tmpPostgres.hostname,
        "PORT": tmpPostgres.port or 5432,
        "OPTIONS": dict(parse_qsl(tmpPostgres.query)),
    }
}


# -------------------
# APPS
# -------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]


# -------------------
# MIDDLEWARE
# -------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# -------------------
# TEMPLATES
# -------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.seo_context",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# -------------------
# PASSWORD VALIDATION
# -------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# -------------------
# LANGUAGE / TIME
# -------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -------------------
# STATIC FILES
# -------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# -------------------
# MEDIA FILES (for uploaded SEO images)
# -------------------
MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# -------------------
# DEFAULT AUTO FIELD
# -------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"