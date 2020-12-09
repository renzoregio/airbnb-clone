from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms
from rooms import models as room_models


def create_review(request, room):
    form = forms.CheckedOutUserReview(request.POST)
    room = room_models.Room.objects.get_or_none(pk=room)
    if not room:
        return redirect(reverse("core:home"))
    if form.is_valid():
        review = form.save()
        review.room = room
        review.user = request.user
        review.save()
        messages.success(request, "Review has been submitted")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
