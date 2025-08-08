import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import from iskcon
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

from django.core.wsgi import get_wsgi_application

# Collect static files during build
try:
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
except:
    pass  # Ignore errors during static collection in serverless environment

app = get_wsgi_application()