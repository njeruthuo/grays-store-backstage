from django.urls import path
from .views import mpesa_callback

urlpatterns = [
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
]
