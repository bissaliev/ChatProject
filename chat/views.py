from django.shortcuts import redirect, render

from .models import Room


def index(request):
    rooms = Room.objects.all()
    return render(request, "chat/index.html", context={"rooms": rooms})


def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "chat/room.html", {"room_name": room_name})
