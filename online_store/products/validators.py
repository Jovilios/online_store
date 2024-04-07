from django.core.exceptions import ValidationError


SIZE_5_MB = 5 * 1024 * 1024


def validate_image_size_less_than_5mb(value):
    if value.size > SIZE_5_MB:
        raise ValidationError('File size should be less than 5MB')