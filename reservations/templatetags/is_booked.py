import datetime
from django import template
from reservations.models import BookedPeriod

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        BookedPeriod.objects.get(period=date, reservation__room=room)
        return True
    except BookedPeriod.DoesNotExist:
        return False
