"""
Production settings for jobsearch project.
"""

from pathlib import Path
import os
import secrets

# Import base settings
from jobsearch.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a new secret key for production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', secrets.token_hex(32))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your domain name(s) here
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database settings
# Use PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'jobsearch_db'),
        'USER': os.environ.get('DB_USER', 'jobsearch_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static_collected')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    # Add your frontend domain(s) here
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}

# Make sure the logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)
