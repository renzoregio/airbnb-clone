from django import forms
from django.forms import ModelForm
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):
    city = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "City"})
    )
    country = CountryField().formfield()
    room_type = forms.ModelChoiceField(
        queryset=models.RoomType.objects.all(),
        required=False,
    )
    price = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "Amount"})
    )
    beds = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "No. of Beds"})
    )
    guests = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "No. of Guests"})
    )
    bedrooms = forms.IntegerField(
        required=False, widget=forms.TextInput(attrs={"placeholder": "No. of Bedrooms"})
    )
    bathrooms = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "No. of Bathrooms"}),
    )


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "file",
            "caption",
        )

    def save(self, room_pk, *args, **kwargs):
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=room_pk)
        photo.room = room
        photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
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

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        return room