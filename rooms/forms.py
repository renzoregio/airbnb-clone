from django import forms
from django_countries.fields import CountryField
from . import models

class SearchForm(forms.Form):
    city = forms.CharField(required=False, initial="Anywhere")
    country = CountryField().formfield()
    room_type = forms.ModelChoiceField(queryset=models.RoomType.objects.all(), required=False)
    price = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)
    amenities = forms.ModelMultipleChoiceField(queryset=models.Amenity.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    facilities = forms.ModelMultipleChoiceField(queryset=models.Facility.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    house_rules = forms.ModelMultipleChoiceField(queryset=models.HouseRule.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
