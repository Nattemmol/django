from rest_framework import generics, permissions
from .models import ChatRoom, Message, Notification, ForumThread
from .serializers import ChatRoomSerializer, MessageSerializer, NotificationSerializer, ForumThreadSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils import timezone

User = get_user_model()

class ChatRoomListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(users=self.request.user)

    def perform_create(self, serializer):
        room = serializer.save()
        room.users.add(self.request.user)

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        room = get_object_or_404(ChatRoom, id=room_id)
        if self.request.user not in room.users.all():
            raise PermissionDenied("You are not a participant of this chat room.")
        messages = Message.objects.filter(room=room).order_by('sent_at')
        # Mark messages as read
        for message in messages:
            message.read_by.add(self.request.user)
        return messages

    def perform_create(self, serializer):
        room_id = self.kwargs['room_id']
        room = get_object_or_404(ChatRoom, id=room_id)
        if self.request.user not in room.users.all():
            raise PermissionDenied("You are not a participant of this chat room.")
        serializer.save(sender=self.request.user, room=room)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        notifications = Notification.objects.filter(user=self.request.user)
        # Mark notifications as read
        notifications.update(read=True, seen_at=timezone.now())
        return notifications

class ForumThreadCreateView(generics.CreateAPIView):
    serializer_class = ForumThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ForumThreadListView(generics.ListAPIView):
    serializer_class = ForumThreadSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        topic = self.kwargs['topic']
        return ForumThread.objects.filter(topic=topic)
