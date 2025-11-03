# Import required modules for configuration
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Set the base directory of the project (two levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# GeoDjango library paths - only needed on Windows
# Windows requires explicit paths to GDAL and GEOS DLLs for spatial operations
if sys.platform == 'win32':
    GDAL_LIBRARY_PATH = r'C:\Users\patri\miniconda3\envs\lbs_app\Library\bin\gdal.dll'
    GEOS_LIBRARY_PATH = r'C:\Users\patri\miniconda3\envs\lbs_app\Library\bin\geos_c.dll'
# On Linux (Docker), system packages are used automatically

# Django security and environment settings
SECRET_KEY = os.getenv("SECRET_KEY", "padzerpadzerpadzerpadzer")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")

# Installed Django applications
INSTALLED_APPS = [
    "django.contrib.admin",          # Admin interface
    "django.contrib.auth",           # Authentication system
    "django.contrib.contenttypes",   # Content types framework
    "django.contrib.sessions",       # Session framework
    "django.contrib.messages",       # Messaging framework
    "django.contrib.staticfiles",    # Static file handling
    "django.contrib.gis",            # GeoDjango for spatial database support
    "rest_framework",                # Django REST Framework for API
    "django_filters",                # Advanced filtering for APIs
    "corsheaders",                   # Cross-Origin Resource Sharing support
    "lbs_app",                       # Our main application
]

# Middleware that processes requests/responses in order
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",        # Security enhancements
    "whitenoise.middleware.WhiteNoiseMiddleware",           # Serve static files efficiently
    "django.contrib.sessions.middleware.SessionMiddleware", # Enable sessions
    "corsheaders.middleware.CorsMiddleware",                # Handle CORS headers
    "django.middleware.common.CommonMiddleware",            # Common utilities
    "django.middleware.csrf.CsrfViewMiddleware",            # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # User authentication
    "django.contrib.messages.middleware.MessageMiddleware",     # Flash messages
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
]

# Root URL configuration file
ROOT_URLCONF = "lbs_project.urls"

# Template engine configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "lbs_app" / "templates"],  # Look for templates in lbs_app/templates
        "APP_DIRS": True,                              # Also look in each app's templates folder
        "OPTIONS": {
            # Context processors add variables available to all templates
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application for serving Django
WSGI_APPLICATION = "lbs_project.wsgi.application"
# ASGI application for async web servers
ASGI_APPLICATION = "lbs_project.asgi.application"

# Database configuration using PostGIS for spatial data
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",  # Use PostGIS backend for spatial support
        "NAME": os.getenv("DB_NAME", "lbs_db"),              # Database name
        "USER": os.getenv("DB_USER", "postgres"),            # Database user
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),    # Database password
        "HOST": os.getenv("DB_HOST", "localhost"),           # Database host (localhost or docker service name)
        "PORT": os.getenv("DB_PORT", "5432"),                # Database port
    }
}

# Password validation rules
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Dublin"  # Set timezone to Dublin
USE_I18N = True              # Enable internationalization
USE_TZ = True                # Use timezone-aware datetimes

# Static files configuration
STATIC_URL = "/static/"                                    # URL prefix for static files
STATICFILES_DIRS = [BASE_DIR / "lbs_app" / "static"]      # Where to find static files during development
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "staticfiles")  # Where to collect static files for production

# Use BigAutoField as default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",  # Advanced filtering
        "rest_framework.filters.SearchFilter",                 # Search functionality
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",           # JSON response format
        "rest_framework.renderers.BrowsableAPIRenderer",   # HTML browsable API
    ],
}

# CORS (Cross-Origin Resource Sharing) settings
# Allow requests from these origins to access the API
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8000").split(",")