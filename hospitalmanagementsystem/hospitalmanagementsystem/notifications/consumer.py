from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("✅ WebSocket CONNECTED:", self.channel_name)

        self.group_name = "receptionists"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("❌ WebSocket DISCONNECTED:", self.channel_name)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        print("📨 EVENT RECEIVED:", event["message"])
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
