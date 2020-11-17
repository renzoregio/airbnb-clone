import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from users.models import User
from rooms import models as rooms_models
from lists import models as list_models


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,
            default=1,
            help="How many lists do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        user = User.objects.all()
        rooms = rooms_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(user),
            },
        )
        created = seeder.execute()
        list_id = flatten(list(created.values()))
        for pk in list_id:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(1, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)
        self.stdout.write(self.style.SUCCESS(f"{number} lists have been created"))
