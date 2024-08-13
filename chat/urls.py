from django.urls import path

from .views import index, room

app_name = "chat"

urlpatterns = [
    path("", index, name="home"),
    path("chat/room/<slug:room_name>/", room, name="room"),
]
