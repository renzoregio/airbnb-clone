from django.urls import reverse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from . import models as room_models, forms


class HomeView(ListView):
    model = room_models.Room
    paginate_by = 10
    paginate_orphans = 7 
    context_object_name = "rooms"


def room_detail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", context={"room":room})
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
            instant_book = form.cleaned_data.get("instant_book")
            superhost = form.cleaned_data.get("superhost")
            amenities = form.cleaned_data.get("amenities")
            facilities = form.cleaned_data.get("facilities")
            house_rules = form.cleaned_data.get("house_rules")

            filter_args = {}

            if city != "Anywhere":
                filter_args["city"] = city
            
            filter_args["country"] = country

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
            
            if instant_book is True:
                filter_args["instant_book"] = True

            if superhost is True:
                filter_args["host__superhost"] = True
            
            for amenity in amenities:
                filter_args["amenities"] =  amenity
            
            for facility in facilities:
                filter_args["facilities"] = facility
            
            for rule in house_rules:
                filter_args["house_rules"] = rule

            rooms = room_models.Room.objects.filter(**filter_args).order_by("-created")
            page = request.GET.get("page")
            paginator = Paginator(rooms, 10, orphans=5)
            pages = paginator.get_page(page)
            return render(request, "rooms/search.html", context={"form": form, "pages": pages})

    else:
        form = forms.SearchForm()

    return render(request, "rooms/search.html", context={"form": form})








