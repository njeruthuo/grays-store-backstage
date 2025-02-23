from django.urls import re_path
from .consumers import  MPESAConsumer

websocket_urlpatterns = [
    re_path(r"wss/mpesa/$", MPESAConsumer.as_asgi()),
]
