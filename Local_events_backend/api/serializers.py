from rest_framework import serializers
from .models import Category, Event, Guest, User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon_name']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'image_path', 'title', 'description', 'location', 'date', 'duration', 'punch_line1', 'punch_line2', 'host', 'categories', 'gallery_images', 'guests']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['id', 'name', 'email', 'image_path']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'display_name', 'image_path', 'is_staff', 'is_superuser']
