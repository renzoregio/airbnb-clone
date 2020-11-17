from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Model Definition """

    list_display = (
        "room",
        "status",
        "guest",
        "check_in",
        "check_out",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)
