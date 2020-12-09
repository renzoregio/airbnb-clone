from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>",
        views.create_reservation,
        name="create-reservation",
    ),
    path(
        "<int:pk>/reservation-detail",
        views.ReservationDetailView.as_view(),
        name="detail",
    ),
    path("<int:pk>/<str:action>", views.edit_reservation, name="edit"),
    path("<int:pk>", views.reservations_list.as_view(), name="reservations-list"),
]
