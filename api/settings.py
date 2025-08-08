# api/settings.py
# This file imports and extends your existing settings for Vercel compatibility

import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import from iskcon
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Import all settings from your existing iskcon.settings
from iskcon.settings import *

# Override/add Vercel-specific settings
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', 'localhost', '*']

# Static files configuration for Vercel
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# WSGI application for Vercel
WSGI_APPLICATION = 'api.wsgi.app'

# Database - you can override this if needed for production
# For now, it will use whatever is defined in your iskcon/settings.py