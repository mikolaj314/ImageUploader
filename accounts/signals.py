from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import AccountTier, UserAccount


@receiver(post_save, sender=UserAccount)
def create_user_account(sender, instance, created, **kwargs):
    if created and not instance.account_tier:
        instance.account_tier = AccountTier.objects.get(name="BASIC")
        instance.save()
