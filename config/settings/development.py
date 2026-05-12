from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Show emails in terminal during development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Use local file storage during development
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Disable rate limiting in dev
RATELIMIT_ENABLE = False

# Allow all origins in dev
CORS_ALLOW_ALL_ORIGINS = True