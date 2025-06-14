from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from communication.models import Notification

class NotificationService:
    @classmethod
    def send(cls, user, content, notif_type="message"):
        """
        Save the notification and send it via WebSocket.
        This method is synchronous and should be wrapped using database_sync_to_async if called in an async context.
        """
        try:
            notification = Notification.objects.create(
                user=user,
                content=content,
                type=notif_type,
            )

            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                {
                    'type': 'notify',
                    'content': content,
                    'created_at': notification.created_at.isoformat(),
                }
            )

            return notification

        except Exception as e:
            # Log or handle errors (optional)
            print(f"[NotificationService] Error sending notification: {e}")
            return None
