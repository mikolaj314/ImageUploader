import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from images.models import ThumbnailSize


class AccountTier(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=50)
    expiring_link = models.BooleanField(default=False)
    original_file = models.BooleanField(default=False)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_sizes(self):
        return self.thumbnail_sizes.all()

    @property
    def get_available_heights(self):
        thumbnails = self.get_thumbnail_sizes
        return [t.height for t in thumbnails]


class UserAccount(AbstractUser):
    objects = UserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_tier = models.ForeignKey(
        AccountTier, on_delete=models.SET_NULL, null=True, related_name="users"
    )

    def __str__(self):
        return f"{self.username} {self.account_tier.name}"
