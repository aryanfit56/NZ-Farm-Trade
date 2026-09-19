from pathlib import Path
import os
from dotenv import load_dotenv


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY SETTINGS
# ============================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-only-change-me"
)

DEBUG = os.getenv(
    "DJANGO_DEBUG",
    "True"
).lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # FarmShareNZ application
    "sharing.apps.SharingConfig",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # CSRF protection
    "django.middleware.csrf.CsrfViewMiddleware",

    # Authentication
    "django.contrib.auth.middleware.AuthenticationMiddleware",

    # Messages
    "django.contrib.messages.middleware.MessageMiddleware",

    # Clickjacking protection
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# ROOT URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "farmshare.urls"


# ============================================================
# TEMPLATE CONFIGURATION
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates"
        ],

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


# ============================================================
# WSGI APPLICATION
# ============================================================

WSGI_APPLICATION = "farmshare.wsgi.application"


# ============================================================
# MYSQL DATABASE
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",

        # Database name
        "NAME": os.getenv(
            "DB_NAME",
            "farmshare_db"
        ),

        # MySQL username
        "USER": os.getenv(
            "DB_USER",
            "root"
        ),

        # MySQL password
        "PASSWORD": os.getenv(
            "DB_PASSWORD",
            "root"
        ),

        # MySQL host
        "HOST": os.getenv(
            "DB_HOST",
            "localhost"
        ),

        # Default MySQL port
        "PORT": os.getenv(
            "DB_PORT",
            "3306"
        ),

        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# INTERNATIONALISATION
# ============================================================

LANGUAGE_CODE = "en-nz"

TIME_ZONE = "Pacific/Auckland"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# ============================================================
# MEDIA FILES
# Used for uploaded equipment images
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# AUTHENTICATION
# ============================================================

LOGIN_URL = "login"

LOGIN_REDIRECT_URL = "dashboard"

LOGOUT_REDIRECT_URL = "equipment_list"


# ============================================================
# SESSION SECURITY
# ============================================================

# JavaScript cannot access the session cookie
SESSION_COOKIE_HTTPONLY = True

# Helps protect against cross-site request attacks
SESSION_COOKIE_SAMESITE = "Lax"


# ============================================================
# CSRF SECURITY
# ============================================================

CSRF_COOKIE_SAMESITE = "Lax"


# ============================================================
# CLICKJACKING PROTECTION
# ============================================================

X_FRAME_OPTIONS = "DENY"


# ============================================================
# CONTENT TYPE SECURITY
# ============================================================

SECURE_CONTENT_TYPE_NOSNIFF = True


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    # Cookies only sent over HTTPS
    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    # Redirect HTTP to HTTPS
    SECURE_SSL_REDIRECT = True

    # HTTP Strict Transport Security
    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True