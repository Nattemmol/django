from rest_framework import serializers
from .models import ChatRoom, Message, Notification, ForumThread
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ChatRoomSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'users', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    read_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'message', 'attachment', 'sent_at', 'read_by']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'content', 'type', 'read', 'created_at', 'seen_at']

class ForumThreadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ForumThread
        fields = ['id', 'topic', 'content', 'user', 'created_at', 'tags']
