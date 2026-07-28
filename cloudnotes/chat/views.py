from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from itertools import groupby
from datetime import date

from .models import Conversation, Message


@login_required
def inbox(request):
    """
    Show all conversations for logged-in user
    """
    conversations = (
        Conversation.objects
        .filter(participants=request.user)
        .order_by('-updated_at')
    )

    convo_data = []
    for convo in conversations:
        other = convo.other_user(request.user)
        convo_data.append({
            "id": convo.id,
            "other_user": other,
            "last_message": convo.last_message(),
            "unread_count": convo.unread_count_for(request.user),
        })

    context = {
        "conversations": convo_data
    }
    return render(request, "chat/inbox.html", context)


@login_required
def new_chat(request):
    """
    Show users list to start a new chat
    """
    users = User.objects.exclude(id=request.user.id)

    return render(request, "chat/new_chat.html", {
        "users": users
    })


@login_required
def chat_room(request, username):
    """
    Create or redirect to a conversation using username
    """
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect("chat_inbox")

    # Find existing conversation
    conversation = (
        Conversation.objects
        .filter(participants=request.user)
        .filter(participants=other_user)
        .first()
    )

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect("chat_conversation", convo_id=conversation.id)


@login_required
def conversation_detail(request, convo_id):
    """
    Chat conversation detail + send messages
    """
    conversation = get_object_or_404(
        Conversation,
        id=convo_id,
        participants=request.user
    )

    other_user = conversation.other_user(request.user)

    # Send message
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.save()  # updates updated_at
        return redirect("chat_conversation", convo_id=convo_id)

    # Mark messages as read
    conversation.messages.filter(
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    messages = conversation.messages.select_related("sender")

    # Group messages by date (for template)
    messages_by_date = {}
    for msg in messages:
        msg_date = msg.created_at.date()
        messages_by_date.setdefault(msg_date, []).append(msg)

    context = {
        "conversation": conversation,
        "other_user": other_user,
        "messages_by_date": messages_by_date,
    }

    return render(request, "chat/conversation.html", context)