from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import AccountTier

from default_configs import tiers_config


class CustomUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create enterprise acc user
        cls.user_enterprise = get_user_model().objects.create(
            username="enterprise@gmail.com",
            password="secret",
        )
        acccount_tier = AccountTier.objects.get(name="ENTERPRISE")
        cls.user_enterprise.account_tier = acccount_tier

        # create premium acc user
        cls.user_premium = get_user_model().objects.create(
            username="premium@gmail.com",
            password="secret",
        )
        account_tier = AccountTier.objects.get(name="PREMIUM")
        cls.user_premium.account_tier = account_tier

        # create basic acc user
        cls.user_basic = get_user_model().objects.create(
            username="basic@gmail.com",
            password="secret",
        )
        account_tier = AccountTier.objects.get(name="BASIC")
        cls.user_basic.account_tier = account_tier

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@email.com", password="secretpass"
        )
        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="admin", email="admintest@gmail.com", password="secretadminpass"
        )
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admintest@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_account_tier(self):
        self.assertEqual(self.user_basic.account_tier.name, "BASIC")
        self.assertEqual(self.user_premium.account_tier.name, "PREMIUM")
        self.assertEqual(self.user_enterprise.account_tier.name, "ENTERPRISE")

    def test_available_thumbnails(self):
        thumbnail_sizes = {}

        # Loop through the tiers in DEFAULT_TIERS_CONFIG
        for tier, config in tiers_config.items():
            thumbnail_sizes[tier] = [
                size for size in config.get("thumbnail_sizes", {}).values()
            ]

        # Extract specific tiers' thumbnail sizes
        basic_tier_account = thumbnail_sizes.get("BASIC", [])
        premium_tier_account = thumbnail_sizes.get("PREMIUM", [])
        enterprise_tier_account = thumbnail_sizes.get("ENTERPRISE", [])

        current_user_basic = [
            [
                dict(width=e.width, height=e.height)
                for e in self.user_basic.account_tier.get_thumbnail_sizes
            ]
        ]
        current_user_premium = [
            dict(width=e.width, height=e.height)
            for e in self.user_premium.account_tier.get_thumbnail_sizes
        ]
        current_user_enterprise = [
            dict(width=e.width, height=e.height)
            for e in self.user_enterprise.account_tier.get_thumbnail_sizes
        ]

        self.assertEqual(current_user_basic, [basic_tier_account])
        self.assertEqual(current_user_premium, premium_tier_account)
        self.assertEqual(current_user_enterprise, enterprise_tier_account)

    def test_can_get_original_file(self):
        self.assertFalse(self.user_basic.account_tier.original_file)
        self.assertTrue(self.user_premium.account_tier.original_file)
        self.assertTrue(self.user_enterprise.account_tier.original_file)

    def test_can_generate_expiring_links(self):
        self.assertFalse(self.user_basic.account_tier.expiring_link)
        self.assertFalse(self.user_premium.account_tier.expiring_link)
        self.assertTrue(self.user_enterprise.account_tier.expiring_link)

    def test_user_incorrect_account_tier(self):
        self.assertNotEqual(self.user_basic.account_tier.name, "Fake Tier")
