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

    @database_sync_to_async
    def add_participant_to_room(self, room_name, username):
        room = get_object_or_404(Room, room_name=room_name)
        participant = get_object_or_404(User, username=username)
        room.participants.add(participant)

    @database_sync_to_async
    def remove_participant_from_room(self, room_name, username):
        room = get_object_or_404(Room, room_name=room_name)
        participant = get_object_or_404(User, username=username)
        room.participants.remove(participant)

    @database_sync_to_async
    def get_participants(self, room_name):
        users = User.objects.filter(rooms__room_name=room_name)
        return [
            {"username": user.username, "avatar": user.avatar.url}
            for user in users
        ]

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()
        if self.user.is_authenticated:
            await self.add_participant_to_room(
                self.room_name, self.user.username
            )
        users = await self.get_participants(self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list",
                "users": users,
            },
        )

    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.remove_participant_from_room(
                self.room_name, self.user.username
            )
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        users = await self.get_participants(self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list",
                "users": users,
            },
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
                "avatar": new_msg.sender.avatar.url,
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
                    "avatar": event["avatar"],
                }
            )
        )

    async def user_list(self, event):
        await self.send(
            text_data=json.dumps(
                {"type": "user_list", "users": event["users"]}
            )
        )
