from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connection established")
        await self.accept() # Accepts the connection and allows communication to begin

    async def disconnect(self, code):
        print(f"Connection closed with code: {code}")

    async def receive(self, text_data = None, bytes_data = None):
        message = "No message received" # Initialize default message

        if text_data is not None:
            text_data_json = json.loads(text_data) # Parse the incoming JSON

            # Extract the message content

            # Use .get() to avoid KeyErrors if "message" is missing
            message = text_data_json.get("message", "Empty message")

            print(f"Received from client: {text_data_json}")

        # Send the response back to the WebSocket
        await self.send(text_data=json.dumps({
            "message": message
        }))
