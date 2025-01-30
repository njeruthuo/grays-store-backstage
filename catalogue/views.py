from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


category_api_view = CategoryAPIView.as_view()
