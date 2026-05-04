import random
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Statistic, DataItem

# Celery task that generates a random "System Health" number every 5 seconds
@shared_task
def heartbeat():
    # Generate a random health metric (e.g., latency)
    health_value = random.randint(0, 100)
    
    # Get or create the "System Health" parent object (Statistic)
    # get_or_create ensures the dashboard has a target to display
    statistic, _ = Statistic.objects.get_or_create(
        name="System Health"
    )
    
    # Save the health metric to the database for to be displayed in charts
    DataItem.objects.create(
        statistic=statistic,
        value=health_value,
        owner="System Heartbeat"
    )
    
    # Broadcast the data over WebSocket to all connected clients
    # This allows the UI to update immediately without a page refresh
    channel_layer = get_channel_layer()
    room_group_name = f'stats_{statistic.slug}'
    
    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'sharing_message',
            'value': health_value,
        }
    )
    
    return f"Heartbeat sent: {statistic.name} = {health_value}"
