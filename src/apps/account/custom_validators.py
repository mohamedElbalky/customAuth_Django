
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    # Check if the phone number starts with '0' and has exactly 11 digits
    if not value.startswith('0') or not value.isdigit() or len(value) != 11:
        raise ValidationError('Phone number must start with "0" and contain exactly 11 digits.')