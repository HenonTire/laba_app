import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        user = self.scope.get("user")

        if user is None or user.is_anonymous:
            print("❌ WS rejected: unauthenticated")
            await self.close()
            return

        self.user = user

        # ✅ Make sure room exists
        self.room = await self.get_room(self.room_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"✅ {self.user.username} connected to {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        if not message:
            return

        # ✅ Save message in DB
        saved_message = await self.save_message(
            room=self.room,
            sender=self.user,
            content=message
        )

        # ✅ Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender_id": self.user.id,
                "sender_username": self.user.username,
                "created_at": str(saved_message.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # -----------------------------
    # ✅ Database helper functions
    # -----------------------------

    @database_sync_to_async
    def get_room(self, room_id):
        return ChatRoom.objects.get(id=room_id)

    @database_sync_to_async
    def save_message(self, room, sender, content):
        return Message.objects.create(
            room=room,
            sender=sender,
            content=content
        )
