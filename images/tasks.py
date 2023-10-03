from __future__ import absolute_import, unicode_literals

import os
from io import BytesIO

from celery import shared_task
from PIL import Image as PIL_Image

from images.models import Image


@shared_task
def generate_thumbnail_task(pk: str):
    try:
        instance = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        # Handle the case where the image with the given ID doesn't exist
        return

    filename, ext = os.path.splitext(os.path.basename(instance.image.name))
    image_name = filename.split("/")[-1]
    account_tier = instance.user.account_tier
    thumbnail_sizes = account_tier.get_thumbnail_sizes

    original_image_directory = os.path.dirname(instance.image.path)

    img_file = BytesIO(instance.image.read())
    original_image = PIL_Image.open(img_file)

    for size in thumbnail_sizes:
        thumbnail = original_image.resize((size.width, size.height), PIL_Image.LANCZOS)
        thumbnail_name = f"{image_name}_{size.height}{ext.lower()}"
        thumbnail_path = os.path.join(original_image_directory, thumbnail_name)
        thumbnail.save(
            thumbnail_path, format="JPEG" if ext.lower() == ".jpg" else "PNG"
        )

    return
