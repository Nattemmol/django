import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from communication.services.notification_service import NotificationService
from .models import ChatRoom, Message, Notification
from core.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join the chat group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            if not message:
                await self.send(text_data=json.dumps({'error': 'Message content missing.'}))
                return

            sender_id = self.scope['user'].id
            await self.save_message(self.room_id, sender_id, message)

            receiver = await self.get_other_user(self.room_id, sender_id)
            if receiver:
                # Consider making this async-safe if NotificationService.send is blocking
                await database_sync_to_async(NotificationService.send)(receiver, "📢 New message received!")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': sender_id,
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender_id': event['sender_id'],
        }))

    @database_sync_to_async
    def save_message(self, room_id, sender_id, message):
        try:
            room = ChatRoom.objects.get(id=room_id)
            sender = User.objects.get(id=sender_id)
            return Message.objects.create(room=room, sender=sender, message=message)
        except ChatRoom.DoesNotExist:
            raise Exception("ChatRoom not found.")
        except User.DoesNotExist:
            raise Exception("Sender not found.")

    @database_sync_to_async
    def get_other_user(self, room_id, sender_id):
        try:
            room = ChatRoom.objects.get(id=room_id)
            participants = room.participants.exclude(id=sender_id)
            return participants.first()
        except ChatRoom.DoesNotExist:
            return None


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.group_name = f'notifications_{self.user.id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'content': event['content'],
            'created_at': event['created_at'],
        }))
