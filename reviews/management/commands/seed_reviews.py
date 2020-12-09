import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from rooms import models as room_models
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reviews do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        user = User.objects.all()
        room = room_models.Room.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "user": lambda x: random.choice(user),
                "room": lambda x: random.choice(room),
                "accuracy": lambda x: random.randint(1, 10),
                "communication": lambda x: random.randint(1, 10),
                "cleanliness": lambda x: random.randint(1, 10),
                "location": lambda x: random.randint(1, 10),
                "check_in": lambda x: random.randint(1, 10),
                "value": lambda x: random.randint(1, 10),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} reviews have been created"))
