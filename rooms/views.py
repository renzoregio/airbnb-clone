from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . import models as room_models, forms
from users import mixins


class HomeView(ListView):
    model = room_models.Room
    paginate_by = 12
    paginate_orphans = 7
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", context={"room": room})
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


def search(request):

    country = request.GET.get("country")

    if country:
        form = forms.SearchForm(request.GET)
        if form.is_valid():

            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
            room_type = form.cleaned_data.get("room_type")
            price = form.cleaned_data.get("price")
            beds = form.cleaned_data.get("beds")
            guests = form.cleaned_data.get("guests")
            bedrooms = form.cleaned_data.get("bedrooms")
            baths = form.cleaned_data.get("baths")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city__startswith"] = city

            filter_args["country__startswith"] = country

            if room_type is not None:
                filter_args["room_type"] = room_type

            if price is not None:
                filter_args["price__lte"] = price

            if beds is not None:
                filter_args["beds__gte"] = beds

            if guests is not None:
                filter_args["guests__gte"] = guests

            if bedrooms is not None:
                filter_args["bedrooms__gte"] = bedrooms

            if baths is not None:
                filter_args["baths__gte"] = baths

            rooms = room_models.Room.objects.filter(**filter_args).order_by("-created")
            page = request.GET.get("page")
            paginator = Paginator(rooms, 10, orphans=5)
            pages = paginator.get_page(page)
            return render(
                request,
                "rooms/search.html",
                context={"form": form, "pages": pages, "country": country},
            )

    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", context={"form": form})


class EditRoomView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    template_name = "rooms/edit-room.html"
    model = room_models.Room
    success_message = "Room details have been successfully updated"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "baths",
        "bedrooms",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        host = room.host.pk
        user = self.request.user.pk
        if host == user:
            return room
        else:
            raise Http404()


class UpdateRoomPhotosView(mixins.LoggedInOnlyView, DetailView):

    model = room_models.Room
    template_name = "rooms/edit-photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        host = room.host.pk
        user = self.request.user.pk
        if host == user:
            return room
        else:
            raise Http404()


@login_required
def delete_photo(request, room_pk, photo_pk):
    try:
        user = request.user
        room = room_models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cannot delete that photo")
        else:
            photo = room_models.Photo.objects.get(pk=photo_pk)
            photo.delete()
            messages.success(request, "Photo has been deleted")
        return redirect(reverse("rooms:edit-photos", kwargs={"pk": room_pk}))
    except room_models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = room_models.Photo
    template_name = "rooms/edit-photo.html"
    fields = ("caption",)
    pk_url_kwarg = "photo_pk"
    success_message = " Photo has been updated "

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:edit-photos", kwargs={"pk": room_pk})


class AddPhotoView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.AddPhotoForm
    template_name = "rooms/add-photo.html"

    def form_valid(self, form):
        room_pk = self.kwargs.get("pk")
        form.save(room_pk)
        messages.success(self.request, "Photo has been uploaded")
        return redirect(reverse("rooms:edit-photos", kwargs={"pk": room_pk}))


@login_required
def delete_room(request, pk):
    user = request.user
    room = room_models.Room.objects.get(pk=pk)
    if room.host.pk == user.pk:
        return render(request, "rooms/delete-room.html", context={"room": room})
    else:
        Http404()


@login_required
def delete_room_confirmation(request, pk):
    user = request.user
    room = room_models.Room.objects.get(pk=pk)
    room.delete()
    return redirect(reverse("users:profile", kwargs={"username": user.username}))


class CreateRoomView(mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreateRoomForm
    template_name = "rooms/create-room.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))