from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


from rest_framework.authentication import TokenAuthentication


class Authenticator(TokenAuthentication):
    keyword = 'Bearer'


User = get_user_model()


class EmailOrUsernameBackend(BaseBackend):
    """
    Custom authentication backend to authenticate with either username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        # Check if the input is an email or username
        if "@" in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        # Check password validity
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
