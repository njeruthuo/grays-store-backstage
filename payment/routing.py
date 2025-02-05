from django.urls import re_path
from .consumers import PaymentConsumer, MPESAConsumer

websocket_urlpatterns = [
    re_path(r"ws/payments/$", PaymentConsumer.as_asgi()),
    re_path(r"ws/mpesa/$", MPESAConsumer.as_asgi()),
]
