from django.shortcuts import render, redirect, reverse
from django.views.generic import DetailView
from django.http import Http404
from django.db.models import Q
from users import models as user_models
from . import models, forms


def go_conversation(request, user_username, guest_username, user_pk, guest_pk):
    user_username = user_models.User.objects.get(username=user_username)
    guest_username = user_models.User.objects.get(username=guest_username)
    user = user_models.User.objects.get(pk=user_pk)
    guest = user_models.User.objects.get(pk=guest_pk)
    if user is not None and guest is not None:
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user) & Q(participants=guest)
            )
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user, guest)
        return redirect(
            reverse(
                "conversations:detail",
                kwargs={
                    "pk": conversation.pk,
                    "user_pk": user.pk,
                    "guest_pk": guest.pk,
                },
            )
        )


def conversation_detail(request, pk, guest_pk, user_pk):
    user = user_models.User.objects.get(pk=user_pk)
    guest = user_models.User.objects.get(pk=guest_pk)
    try:
        conversation = models.Conversation.objects.get(pk=pk)
    except models.Conversation.DoesNotExist:
        raise Http404()
    return render(
        request,
        "conversations/conversation_detail.html",
        context={
            "conversation": conversation,
            "user": user,
            "guest": guest,
        },
    )


def send_message(request, guest_pk, user_pk, conversation_pk):
    message = request.POST.get("message", None)
    guest = user_models.User.objects.get(pk=guest_pk)
    user = user_models.User.objects.get(pk=user_pk)
    try:
        conversation = models.Conversation.objects.get(pk=conversation_pk)
    except models.Conversation.DoesNotExist:
        raise Http404()
    if message is not None:
        models.Message.objects.create(
            user=guest, message=message, conversation=conversation
        )
    return redirect(
        reverse(
            "conversations:detail",
            kwargs={
                "pk": conversation.pk,
                "user_pk": user.pk,
                "guest_pk": guest.pk,
            },
        )
    )
