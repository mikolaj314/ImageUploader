from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a test user with superuser privileges"

    def handle(self, *args, **options):
        username = "hexadmin"
        password = "hexadmin"
        email = "hex@admin.com"
        if not get_user_model().objects.filter(username=username).exists():
            get_user_model().objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser with username "{username}" '
                    f'and password "{password}.'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'User "{username}" already exists.'
                    f"Please choose a different username."
                )
            )
