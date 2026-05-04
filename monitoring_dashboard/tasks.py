import random
from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Statistic, DataItem

# Celery task that generates a random "System Health" number every 5 seconds
@shared_task
def heartbeat():
    # Fetch all devices that are currently in the DB
    all_statistics = Statistic.objects.all()
    channel_layer = get_channel_layer()

    for stat in all_statistics:
        # Generate a random health metric (e.g., latency)
        health_value = random.randint(0, 100)

        # Save the health metric to the database for to be displayed in charts
        DataItem.objects.create(
            statistic=stat,
            value=health_value,
            owner="System Heartbeat"
        )

        # Broadcast the data for THIS device over WebSocket to all connected clients
        # The same 'stats_' + slug logic as in Consumers.py
        room_group_name = f'stats_{stat.slug}'

        async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            'type': 'sharing_message',
            'value': health_value,
        }
    )
    
    return f"Heartbeat sent to {all_statistics.count()} devices."