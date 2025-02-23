from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get user information
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        key = request.query_params.get('key')

        # User Login (Sign-in)
        if key == 'sign-in':
            username_or_email = request.data.get(
                'email')
            password = request.data.get('password')

            if not username_or_email or not password:
                return Response({'error': 'Username/Email and Password are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if input is email or username
            user = authenticate(
                request, username=username_or_email, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # User Registration (Sign-up)
        elif key == 'sign-up':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if not username:
                username = email

            if not username or not email or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

            # Create new user
            user = User.objects.create_user(
                username=username, email=email, password=password)

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'UNAUTHORIZED': 'PERMISSION DENIED'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Edit user info
        return Response({}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Delete user or other related info
        return Response({}, status=status.HTTP_200_OK)


user_api_view = UserAPIView.as_view()
