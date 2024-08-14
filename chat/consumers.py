import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Message, Room

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def create_message(self, message, username):
        room = get_object_or_404(Room, room_name=self.room_name)
        user = get_object_or_404(User, username=username)
        new_msg = Message.objects.create(
            sender=user, content=message, room=room
        )
        return new_msg

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        new_msg = await self.create_message(message, username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": new_msg.content,
                "username": new_msg.sender.username,
                "created_at": new_msg.created_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        # отправить сообщение в веб-сокет
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "username": event["username"],
                    "message": event["message"],
                    "created_at": event["created_at"],
                }
            )
        )
