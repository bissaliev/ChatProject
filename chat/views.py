from django.shortcuts import redirect, render

from .models import Room


def index(request):
    rooms = Room.objects.all()
    return render(request, "chat/index.html", context={"rooms": rooms})


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect("login")
    current_room = Room.objects.get(room_name=room_name)
    messages = current_room.messages.all().order_by("created_at")
    participants = current_room.participants.all().exclude(
        username=request.user.username
    )
    return render(
        request,
        "chat/room.html",
        {
            "room_name": room_name,
            "current_room": current_room,
            "messages": messages,
            "participants": participants,
        },
    )
