from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("create/room/", views.CreateRoomView.as_view(), name="create"),
    path("<int:pk>/", views.room_detail, name="detail"),
    path("search/", views.search, name="search"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit-room"),
    path(
        "<int:pk>/edit/photos", views.UpdateRoomPhotosView.as_view(), name="edit-photos"
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("<int:pk>/photos/add/", views.AddPhotoView.as_view(), name="add-photo"),
    path("<int:pk>/delete-room/", views.delete_room, name="delete-room"),
    path(
        "<int:pk>/delete-room-confirmation/",
        views.delete_room_confirmation,
        name="delete-confirmation",
    ),
]
