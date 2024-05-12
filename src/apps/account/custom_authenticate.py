from django.contrib.auth.backends import ModelBackend

from .models import User


class EmailPhoneNumberAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        return None