import os
import sys

# Ensure the Django project directory is in Python path for Vercel serverless execution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudnotes.settings')

application = get_wsgi_application()
app = application

