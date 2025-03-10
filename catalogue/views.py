from django.db.transaction import atomic
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


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


class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.select_related('brand', 'category')
        serializer_data = ProductSerializer(products, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)
    
    # Pagination required here

    @atomic
    def post(self, request, *args, **kwargs):
        data = request.data.copy()  # Make a mutable copy

        brand_name = data.pop("brand", None)
        category_name = data.pop("category", None)

        images = request.FILES.getlist("images")
        print("Received Images:", images)

        # Get or create brand & category
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        category, _ = Category.objects.get_or_create(name=category_name)

        # Create product instance
        product = Product.objects.create(
            brand=brand, category=category, **data
        )

        # Correct way to add images
        image_objects = [Image(product=product, image=image)
                         for image in images]
        Image.objects.bulk_create(image_objects)  # Efficient image saving

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
