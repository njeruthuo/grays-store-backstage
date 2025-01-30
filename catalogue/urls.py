from django.urls import path
from .views import category_api_view


urlpatterns = [
    path('category_api_view/', category_api_view, name='category_api_view'),
]
