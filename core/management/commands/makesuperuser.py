from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Command to create a superuser"

    def handle(self, *args, **options):
        username = settings.SUPERUSER_USERNAME
        password = settings.SUPERUSER_PASSWORD
        User = get_user_model() # noqa
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, password=password, is_active=True
            )
            msg = self.style.SUCCESS(f"Admin {username} was created")
        else:
            msg = self.style.NOTICE(f"Admin {username} already exists")
        self.stdout.write(msg)