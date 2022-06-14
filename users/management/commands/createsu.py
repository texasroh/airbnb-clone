from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "Thish command creates superuser"

    def handle(self, *args, **kwargs):
        admin = User.objects.get_or_none(is_superuser=True)
        if not admin:
            User.objects.create_superuser("admin", "", "admin")
            self.stdout.write(self.style.SUCCESS("Superuser created!"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser exist!"))
