from django.urls import path

from .views import user_api_view


urlpatterns = [
    path('user_api_view/', user_api_view, name='user_api_view'),
]
