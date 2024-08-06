from django.contrib.auth.backends import BaseBackend
from .models import User
from django.contrib.auth.hashers import check_password

class MongoEngineUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Attempt to retrieve user by email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # Check if the user is active and if the password matches
        if user and user.is_activated and check_password(password, user.password):
            return user  # Authentication successful
        return None  # Authentication failed

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None