from django.shortcuts import redirect, reverse, render
from django.contrib import messages
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models
from users.models import User


def toggle_room(request, room_pk, action):
    room = room_models.Room.objects.get(pk=room_pk)
    if room is not None:
        the_list, created = models.List.objects.get_or_create(
            user=request.user,
            name="My Favorite Houses",
        )
        if action == "add":
            the_list.rooms.add(room)
            messages.success(
                request,
                f"You have successfully added {room.name} to your favorite houses list",
            )
        elif action == "remove":
            the_list.rooms.remove(room)
            messages.success(
                request,
                f"You have successfully removed {room.name} from your favorite houses list",
            )
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


def favorite_list(request, username):
    user = request.user
    User.objects.get(username=username)
    return render(request, "lists/fav-list.html", context={"user": user})
