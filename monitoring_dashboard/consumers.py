from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the dashboard slug from the URL (defined in routing.py)
        url_route = self.scope.get('url_route') # Access the route parameters
        if url_route:
            self.dashboard_slug = url_route['kwargs'].get('dashboard_slug', 'default')
        else:
            self.dashboard_slug = 'default' # Fallback if the route isn't found
    
        self.room_group_name = f'stats_{self.dashboard_slug}'

        # Join the group
        # This allows multiple users to view the same dashboard and receive the same updates
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print(f"Connection established to group: {self.room_group_name}")
        await self.accept()

    async def disconnect(self, code):
        # Leave the group when the browser tab is closed
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Connection closed for group: {self.room_group_name}")

    # This method is triggered when a user types a value into the "ManualHealth Input" on the UI
    # and clicks "Send"
    async def receive(self, text_data = None, bytes_data = None):
        if text_data:
            text_data_json = json.loads(text_data) # Parse the incoming JSON
            # Extract a value (latency) from the UI.
            # Use .get() to avoid KeyErrors if "message" is missing
            value = text_data_json.get("message", 0)
        
        # Broadcast the message to every client in the group
        # This triggers the 'sharing_message' method below for all connected clients
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'sharing_message',
                    'value': value,
                }
            )
    
    # This method sends the actual data to the WebSocket. It's called for every user in the group.
    async def sharing_message(self, event):
        value = event['value']

        # Send data to the UI in the format the Chart.js expects
        await self.send(text_data=json.dumps({
            'value': value,
            'time': None # dashboard.js will generate a timestamp if this is None
        }))
