from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):
    help = "This command creates rooms"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--number",
            default=2,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        seeder.add_entity(room_models.Room, number, {""})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!"))
