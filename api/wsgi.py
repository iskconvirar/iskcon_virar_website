import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import from iskcon
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iskcon.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()