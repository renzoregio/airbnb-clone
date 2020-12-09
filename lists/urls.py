from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:room_pk>/<str:action>", views.toggle_room, name="toggle-room"),
    path("<str:username>/favorites/", views.favorite_list, name="favorite-list"),
]
