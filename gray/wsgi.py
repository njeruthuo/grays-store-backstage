"""
WSGI config for gray project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings  # ✅ Correct import
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gray.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(
    settings.BASE_DIR, 'staticfiles'))

app = application  # Only needed for some hosting services (e.g., Vercel)
