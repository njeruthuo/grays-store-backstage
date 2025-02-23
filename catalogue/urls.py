from django.urls import path
from .views import category_api_view, product_api_view, brand_api_view


urlpatterns = [
    path('category_api_view/', category_api_view, name='category_api_view'),
    path('product_api_view/', product_api_view, name='product_api_view'),
    path('brand_api_view/', brand_api_view, name='brand_api_view'),

]
