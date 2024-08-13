from django.shortcuts import redirect, render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_id):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "chat/room.html", {"room_id": room_id})
