from dotenv import load_dotenv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gray.settings")
django.setup()

import payment.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter


load_dotenv()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(payment.routing.websocket_urlpatterns),
})
