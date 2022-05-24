import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

NAME = "lists"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--number", default=2, type=int, help=f"How many {NAME} you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )
        created_reviews = seeder.execute()
        created_clean = flatten(list(created_reviews.values()))
        for pk in created_clean:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = random.sample(list(rooms), random.randint(5, 30))
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!"))
