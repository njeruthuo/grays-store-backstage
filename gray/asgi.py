import os
import payment.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import dotenv

dotenv.read_dotenv()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(payment.routing.websocket_urlpatterns),
})

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gray.settings")
