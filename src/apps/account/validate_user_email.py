import secrets

from django.contrib.auth import get_user_model
from .models import VerificationToken


def generate_verification_token(email):
    token = secrets.token_hex(32)
    # --------- delete old token for email -------
    old_tokens = VerificationToken.objects.filter(email=email)
    old_tokens.delete()
    # --------------------------------------------
    VerificationToken.objects.create(email=email, token=token)
    return token


def get_email_from_token(token):
    try:
        obj = VerificationToken.objects.get(token=token)
        return obj.email
    except VerificationToken.DoesNotExist:
        return None


def verify_user_email(email):
    try:
        user = get_user_model().objects.get(email=email)
    except get_user_model().DoesNotExist:
        return False

    user.is_verified = True
    user.save()

    return True
