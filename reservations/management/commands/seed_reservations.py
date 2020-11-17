import random
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django_seed import Seed
from rooms import models as rooms_models
from users.models import User
from reservations import models as reservations_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many reservations do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        user = User.objects.all()
        rooms = rooms_models.Room.objects.all()
        status = reservations_models.Status.objects.all()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            {
                "guest": lambda x: random.choice(user),
                "status": lambda x: random.choice(status),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(5, 100)),
            },
        )
        seeder.execute()
        self.stdout.write(
            self.style.SUCCESS(f"{number} reservations have been created!")
        )
