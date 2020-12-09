import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from . import models
from rooms import models as room_models
from reviews import forms as review_forms


class CreateError(Exception):
    pass


def create_reservation(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedPeriod.objects.get(period=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Unable to access the room")
        return redirect(reverse("core:home"))
    except models.BookedPeriod.DoesNotExist:
        reservation = models.Reservation.objects.create(
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
            guest=request.user,
            room=room,
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        review_form = review_forms.CheckedOutUserReview()
        if not reservation or (
            reservation.guest != self.request.user
            and room_models.Room.host != self.request.user
        ):
            raise Http404()
        return render(
            self.request,
            "reservations/reservation-detail.html",
            context={"reservation": reservation, "review_form": review_form},
        )


def edit_reservation(request, pk, action):
    try:
        reservation = models.Reservation.objects.get(pk=pk)
        if action == "confirm":
            reservation.status = models.Reservation.STATUS_CONFIRMED
        elif action == "cancel":
            reservation.status = models.Reservation.STATUS_CANCELLED
            models.BookedPeriod.objects.filter(reservation=reservation).delete()
        reservation.save()
        messages.success(request, "Reservation status has been updated")
        return redirect(reverse("rooms:detail", kwargs={"pk": reservation.room.pk}))
    except models.Reservation.DoesNotExist:
        if reservation.room.host != request.user and reservation.guest != request.user:
            raise Http404()


class reservations_list(View):
    def get(self, *args, **kwargs):
        reservations = models.Reservation.objects.all().order_by("created")
        user = self.request.user
        return render(
            self.request,
            "reservations/reservations-list.html",
            context={"reservations": reservations, "user": user},
        )
