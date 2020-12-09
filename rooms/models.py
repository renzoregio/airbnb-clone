from django.utils import timezone
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)
    description = models.CharField(max_length=80, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
        return self.description


class RoomType(AbstractItem):

    """ RoomType Model Definition"""

    class Meta:
        verbose_name = "Room Type"

    pass


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"

    pass


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"

    pass


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"

    pass


class Photo(core_models.TimeStampedModel):

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    bedrooms = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)  # Call the real save() method

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        try:
            for review in all_reviews:
                if all_reviews != 0:
                    all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews), 2)
        except Exception:
            return 0

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def first_photo(self):
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except ValueError:
            return None

    def next_four(self):
        try:
            (photos) = self.photos.all()[1:5]
            return photos
        except ValueError:
            return None

    def get_calendars(self):
        now = timezone.now()
        current_year = now.year
        current_month = now.month
        following_month = 1
        if current_month == 12:
            following_month == 1
        else:
            following_month = current_month + 1
        current_month = Calendar(current_year, current_month)
        next_month = Calendar(current_year, following_month)
        return [current_month, next_month]
