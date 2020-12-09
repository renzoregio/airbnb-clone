import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models


class BookedPeriod(core_models.TimeStampedModel):
    period = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = "Booked Period"

    def __str__(self):
        return str(self.period)


class Reservation(core_models.TimeStampedModel):

    """ Review Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )
    status = models.CharField(
        choices=STATUS_CHOICES, default=STATUS_PENDING, max_length=18
    )

    def __str__(self):
        return f"{self.room}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedPeriod.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if self.pk is None:
            checked_in = self.check_in
            checked_out = self.check_out
            difference = checked_out - checked_in
            existing_reservation = BookedPeriod.objects.filter(
                period__range=(checked_in, checked_out), reservation=self
            )
            if not existing_reservation:
                super().save(*args, **kwargs)
                for date in range(difference.days + 1):
                    day = checked_in + timezone.timedelta(days=date)
                    BookedPeriod.objects.create(period=day, reservation=self)
                return
        return super().save(*args, **kwargs)
