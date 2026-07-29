"""
WSGI config for cloudnotes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloudnotes.settings')

application = get_wsgi_application()

# Run migrations and seed default user automatically on Vercel serverless environment
if os.getenv("VERCEL") == "1" or os.getenv("VERCEL_ENV") is not None:
    try:
        from django.core.management import call_command
        call_command('migrate', interactive=False)
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='YASH')
        if created or not user.check_password('123vardhan'):
            user.set_password('123vardhan')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("Auto-seeded user YASH with requested password.")
    except Exception as e:
        print(f"Serverless auto-migration/seed note: {e}")

