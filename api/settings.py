# api/settings.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from iskcon.settings import *

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', 'localhost', '*']
USE_SUPABASE_STORAGE = os.getenv('USE_SUPABASE_STORAGE', 'False').lower() == 'true'

# Keep the same STATIC_URL, STATICFILES_DIRS, STATIC_ROOT from iskcon/settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

if USE_SUPABASE_STORAGE:
    DEFAULT_FILE_STORAGE = 'iskconapp.storage_backends.SupabaseStorage'

# Remove or comment out the local MEDIA settings when using Supabase
if not USE_SUPABASE_STORAGE:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'


if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

WSGI_APPLICATION = 'api.wsgi.app'
