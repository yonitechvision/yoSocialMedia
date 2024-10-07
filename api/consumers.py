from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate user before allowing the connection
        if self.scope["user"].is_authenticated:
            # Accept the connection
            await self.accept()
            self.room_name = 'room_name'  # Set the room name
            self.room_group_name = f'chat_{self.room_name}'

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        else:
            # Reject the connection if not authenticated
            await self.close()

    async def disconnect(self, close_code):
        # Leave the room group on disconnect
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope["user"].username
            }
        )

    async def chat_message(self, event):
        # Receive the message from the group
        message = event['message']
        user = event['user']

        # Send the message back to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))
