from django.core.validators import MaxValueValidator
from django.db import models
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    communication = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    cleanliness = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    location = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    check_in = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    value = models.IntegerField(validators=[MaxValueValidator(5)], default=5)
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Average"
