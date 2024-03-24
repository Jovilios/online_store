import re

from django.core.exceptions import ValidationError


def validate_password_strength(value):
    if not re.search(r'[A-Z]', value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'"|,.<>/?]', value):
        raise ValidationError("Password must contain at least one special character.")
