from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get user information
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Create an account / login
        return Response({}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # Edit user info
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Delete user or other related info
        return Response({}, status=status.HTTP_200_OK)


user_api_view = UserAPIView.as_view()
