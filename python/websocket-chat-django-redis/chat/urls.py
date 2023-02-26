from django.urls import path
from .views import ChatRoomListView, ChatRoomView

urlpatterns = [
    path('', ChatRoomListView.as_view(), name="chat_room_list"),
    path('chat/<username>', ChatRoomView.as_view(), name="chat_room")
]
