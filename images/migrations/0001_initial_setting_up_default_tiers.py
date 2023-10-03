from django.db import migrations

from default_configs import tiers_config


def create_tiers(apps, schema_editor):
    AccountTier = apps.get_model("accounts", "AccountTier")
    ThumbnailSize = apps.get_model("images", "ThumbnailSize")

    for tier_name, tier_data in tiers_config.items():
        default_tier = AccountTier.objects.create(
            name=tier_name,
            original_file=tier_data["original_file"],
            expiring_link=tier_data["expiring_link"],
        )
        thumbnails = tier_data["thumbnail_sizes"]
        for thumbnail_name, thumbnail_info in thumbnails.items():
            width = thumbnail_info["width"]
            height = thumbnail_info["height"]
            default_thumbnail, _ = ThumbnailSize.objects.get_or_create(
                width=width, height=height
            )
            default_tier.thumbnail_sizes.add(default_thumbnail)


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_initial"),
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_tiers),
    ]
