"""
WSGI config for gray project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import BASE_DIR
import os
from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gray.settings')

application = get_wsgi_application()

application = WhiteNoise(
    application, root=os.path.join(BASE_DIR, 'staticfiles'))

app = application
