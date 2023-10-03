import os
import uuid
import time

from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models

from images.utils import image_upload_path
from images.validators import validate_expiration_time, validate_image_extension


class ThumbnailSize(models.Model):
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.width} x {self.height}"


class Image(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(
        upload_to=image_upload_path, validators=[validate_image_extension]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.image}"

    @property
    def get_original_url(self):
        return self.image.url

    def get_thumbnails(self):
        user_account_tier = self.user.account_tier
        available_thumbnail_sizes = user_account_tier.get_available_heights

        base_file = os.path.dirname(self.image.name)
        storage = default_storage
        thumbnails = storage.listdir(base_file)[1]

        thumbnails_to_return = []
        for thumbnail in thumbnails:
            name, _ = thumbnail.rsplit(".", 1)
            height = name.split("_")[-1]

            if height.isdigit() and int(height) in available_thumbnail_sizes:
                path_to_thumbnail = os.path.join(base_file, thumbnail)
                thumbnails_to_return.append(path_to_thumbnail)

        if user_account_tier.original_file:
            thumbnails_to_return.append(self.get_original_url)

        if user_account_tier.expiring_link and hasattr(self, "expiring_link"):
            thumbnails_to_return.append(self.expiring_link.link)

        return thumbnails_to_return


class ExpiringLink(models.Model):
    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(
        Image, on_delete=models.CASCADE, related_name="expiring_link", unique=True
    )
    link = models.CharField(max_length=255)
    expires_in = models.IntegerField(validators=[validate_expiration_time])

    def __str__(self):
        return f"{self.link} - {self.image}"

    def is_expired(self):
        current_time = time.time()
        return current_time > self.expires_in
