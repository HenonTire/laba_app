import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatRoom, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")

        # ❌ Reject anonymous users
        if user is None or user.is_anonymous:
            print("❌ WS rejected: unauthenticated")
            await self.close()
            return

        self.user = user

        # ✅ Always use ONE global room
        self.room = await self.get_global_room()

        # ✅ Single group name forever
        self.room_group_name = "global_chat"

        # Join group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"✅ {self.user.username} connected to GLOBAL CHAT")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"🔴 {self.user.username} disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")

        # Prevent empty messages
        if not message or not message.strip():
            return

        # ✅ Save message in DB
        saved_message = await self.save_message(message)

        # ✅ Broadcast message to everyone
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": saved_message.content,
                "sender": self.user.username,
                "created_at": str(saved_message.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    # -------------------------
    # DB Helper Functions
    # -------------------------

    @database_sync_to_async
    def get_global_room(self):
        """
        Always return the same room:
        id=1
        """
        room, created = ChatRoom.objects.get_or_create(
            id=1,
            defaults={"name": "Global Chat Room"}
        )
        return room

    @database_sync_to_async
    def save_message(self, content):
        """
        Save message into DB
        """
        return Message.objects.create(
            room=self.room,
            sender=self.user,
            content=content
        )
