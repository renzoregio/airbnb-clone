from django import template
from lists.models import List

register = template.Library()


@register.simple_tag(takes_context=True)
def on_list(context, room):
    user = context.request.user
    the_list, _ = List.objects.get_or_create(user=user, name="My Favorite Houses")
    return room in the_list.rooms.all()
