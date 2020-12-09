from django.urls import path
from . import views

app_name = "conversations"

urlpatterns = [
    path(
        "<str:user_username>&<str:guest_username>/<int:user_pk>/<int:guest_pk>/",
        views.go_conversation,
        name="go",
    ),
    path(
        "<int:pk>/<int:guest_pk>&<int:user_pk>/",
        views.conversation_detail,
        name="detail",
    ),
    path(
        "<int:conversation_pk>/<int:guest_pk>/<int:user_pk>/add-message",
        views.send_message,
        name="send",
    ),
]
