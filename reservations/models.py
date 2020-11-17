from django.db import models
from django.utils import timezone
from core import models as core_models


class AbstractReservation(core_models.TimeStampedModel):

    """ Abstract Reservation Model Definition """

    status = models.CharField(max_length=12)

    class Meta:
        abstract = True

    def __str__(self):
        return self.status


class Status(AbstractReservation):

    """ Pending Status Model Definition """

    pass


class Reservation(core_models.TimeStampedModel):

    """ Review Model Definition """

    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    status = models.ForeignKey(
        "Status",
        on_delete=models.SET_DEFAULT,
        related_name="reservations",
        default="Pending",
    )

    def __str__(self):
        return f"{self.room}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
