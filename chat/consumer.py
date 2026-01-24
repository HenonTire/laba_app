import json
from channels.generic.websocket import AsyncWebsocketConsumer

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

        # Never trust client sender_id
        sender_id = self.user.id
        sender_username = self.user.username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": sender_id,
                "sender_username": sender_username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

