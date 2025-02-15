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
        products = Product.objects.all()
        serializer_data = ProductSerializer(products, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ProductSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({'SUCCESS': 'PRODUCT CREATION WAS SUCCESSFUL'}, status=status.HTTP_201_CREATED)

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
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


brand_api_view = BrandAPIView.as_view()
