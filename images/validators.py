import os

from django.core.exceptions import ValidationError

import default_configs


MAX_EXPIRY_LINK_TIME = default_configs.MAX_EXPIRY_LINK_TIME
MAX_UPLOAD_SIZE = default_configs.MAX_UPLOAD_SIZE
MIN_EXPIRY_LINK_TIME = default_configs.MIN_EXPIRY_LINK_TIME


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".png"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("File extension error. Please upload JPG or PNG image.")

    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError("File size error. Max 10MB is allowed.")


def validate_expiration_time(value):
    if not MIN_EXPIRY_LINK_TIME <= value <= MAX_EXPIRY_LINK_TIME:
        raise ValidationError(
            f"Expiration time error. Choose between {MIN_EXPIRY_LINK_TIME} "
            f"and {MAX_EXPIRY_LINK_TIME} seconds."
        )
