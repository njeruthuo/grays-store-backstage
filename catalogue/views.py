from rest_framework.pagination import PageNumberPagination
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

from django.db.models import Q


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer_data = CategorySerializer(categories, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


category_api_view = CategoryAPIView.as_view()


class ProductPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 100
    page_size_query_param = 'page_size'


class ProductAPIView(APIView):
    pagination_class = ProductPagination  # Assign the pagination class

    def get(self, request, *args, **kwargs):
        products = Product.objects.prefetch_related('brand', 'category').all()

        search_param = request.query_params.get('search')
        if search_param:
            products = products.filter(name__icontains=search_param)

        # Apply pagination
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serialize paginated results
        serializer = ProductSerializer(paginated_products, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     products = Product.objects.prefetch_related('brand', 'category').all()

    #     search_param = request.query_params.get('search')
    #     if search_param:
    #         products = products.filter(name__icontains=search_param)

    #     serializer = ProductSerializer(products, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @atomic
    def post(self, request, *args, **kwargs):
        data = request.data

        brand_name = data.pop("brand", None)
        category_name = data.pop("category", None)
        images = data.pop("images", [])
        price = data.pop("price", None)
        stocked = data.pop("stocked", False)

        print("Received Images:", images)

        if isinstance(price, list):
            price = price[0]

        from decimal import Decimal
        try:
            price = Decimal(price) if price else None
            stocked = bool(stocked) if stocked else False
        except (ValueError, TypeError):
            return Response({"error": "Invalid price or stock value."}, status=400)

        # Get or create brand & category
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        category, _ = Category.objects.get_or_create(name=category_name)

        # Create product instance
        product = Product.objects.create(
            brand=brand, category=category, price=price, stocked=stocked, **data
        )

        if images:
            image_objects = [Image(product=product, image=image)
                             for image in images]
            Image.objects.bulk_create(image_objects)

        return Response({"SUCCESS": "PRODUCT CREATION WAS SUCCESSFUL"}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        # Update stock operations
        # Add images
        # Edit any important info
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


product_api_view = ProductAPIView.as_view()


class BrandAPIView(APIView):

    def get(self, request, *args, **kwargs):
        brands = Brand.objects.all()
        serializer_data = BrandSerializer(brands, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


brand_api_view = BrandAPIView.as_view()
