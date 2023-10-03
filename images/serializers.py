from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from images.models import Image, ExpiringLink
from images.utils import sanitize_filename
from images.validators import validate_image_extension
from images.tasks import generate_thumbnail_task


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image",)

    def validate_image(self, obj):
        validate_image_extension(obj)
        filename = sanitize_filename(obj.name)
        obj.name = filename
        return obj

    def create(self, validated_data: dict) -> Image:
        validated_data["user"] = self.context["request"].user
        image = Image.objects.create(**validated_data)
        generate_thumbnail_task.delay(image.id)
        return image


class ImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = [
            "image",
        ]

    def get_image(self, obj):
        thumbnails = obj.get_thumbnails()
        thumbnails_to_return = []
        for thumbnail in thumbnails:
            if thumbnail.startswith("/media/"):
                path = "http://127.0.0.1:8000" + thumbnail
            else:
                path = "http://127.0.0.1:8000" + settings.MEDIA_URL + thumbnail
            thumbnails_to_return.append(path)

        return thumbnails_to_return


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ("link",)

    def get_image(self, obj):
        thumbnails = obj.get_thumbnails()
        thumbnails_to_return = []
        for thumbnail in thumbnails:
            if thumbnail.startswith("/media/"):
                path = "http://127.0.0.1:8000" + thumbnail
            else:
                path = "http://127.0.0.1:8000" + settings.MEDIA_URL + thumbnail
            thumbnails_to_return.append(path)

        return thumbnails_to_return


class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ("image", "expires_in")

    def __init__(self, *args, **kwargs):
        super(ExpiringLinkCreateSerializer, self).__init__(*args, **kwargs)

        # Set the choices based on user's images
        user = self.context.get("request").user
        images = Image.objects.filter(user=user)
        self.fields["image"].queryset = images

    def validate_image(self, data):
        if self.context.get("request").user != data.user:
            raise ValidationError("You do not have access to this image")
        return data
