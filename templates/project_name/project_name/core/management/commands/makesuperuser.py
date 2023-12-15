from django.conf import settings
from django.core.management.base import BaseCommand
from {{ project_name }}.users.models import User


class Command(BaseCommand):
    help = "Command to create a superuser"

    def handle(self, *args, **options):
        email = settings.SUPERUSER_EMAIL
        password = settings.SUPERUSER_PASSWORD
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email, password=password, is_active=True
            )
            msg = self.style.SUCCESS(f"Admin {email} was created")
        else:
            msg = self.style.NOTICE(f"Admin {email} already exists")
        self.stdout.write(msg)
