import random
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django_seed import Seed
from rooms import models as room_models
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help="How many rooms do you want to create?",
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        room_types = room_models.RoomType.objects.all()
        all_users = User.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "room_type": lambda x: random.choice(room_types),
                "host": lambda x: random.choice(all_users),
                "beds": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "guests": lambda x: random.randint(1, 5),
            },
        )
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()
        created_photos = seeder.execute()
        room_id = flatten(list(created_photos.values()))
        for pk in room_id:
            room = room_models.Room.objects.get(pk=pk)
            for photo in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1,19)}.webp",
                )
            for amenity in amenities:
                random_num = random.randint(0, 15)
                if random_num % 3 == 0:
                    room.amenities.add(amenity)
            for facility in facilities:
                random_num = random.randint(0, 15)
                if random_num % 2 == 0:
                    room.facilities.add(facility)
            for rule in house_rules:
                random_num = random.randint(0, 15)
                if random_num % 3 == 0:
                    room.house_rules.add(rule)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms have been created!"))
