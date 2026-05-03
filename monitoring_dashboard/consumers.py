from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connection established")
        await self.accept() # Accepts the connection and allows communication to begin

    async def disconnect(self, code):
        print(f"Connection closed with code: {code}")

    async def receive(self, text_data = None, bytes_data = None):
        message = None
        sender = None
        if text_data:
            text_data_json = json.loads(text_data)
            message = text_data_json.get("message")
            sender = text_data_json.get("sender")

        print(f"Received message from {sender}: {message}")

        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))
