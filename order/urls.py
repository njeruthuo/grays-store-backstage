from .views import order_api_view

from django.urls import path


urlpatterns = [
    path('order_api_view/', order_api_view, name='order_api_view'),
]
