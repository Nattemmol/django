from django.urls import path
from .views import (
    ChatRoomListCreateView,
    MessageListCreateView,
    NotificationListView,
    ForumThreadCreateView,
    ForumThreadListView,
)

urlpatterns = [
    path('chat/rooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chat/rooms/<int:room_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('forums/', ForumThreadCreateView.as_view(), name='forumthread-create'),
    path('forums/<str:topic>/', ForumThreadListView.as_view(), name='forumthread-list'),
]
