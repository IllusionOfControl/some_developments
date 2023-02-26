from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Room, Message
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.room_object = Room.objects.get(id=chat_id)
        username = self.scope["user"]
        self.user = get_user_model().objects.get(username=username)
        async_to_sync(self.channel_layer.group_add)(
            self.room_object.room_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_object.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json.get("message", "")
        message = Message.objects.create(user=self.user, room=self.room_object, content=content)

        async_to_sync(self.channel_layer.group_send)(
            self.room_object.room_name,
            {
                "type": "chat_message",
                "id": message.id,
                "message": message.content,
                "username": self.user.username
            }
        )

    def chat_message(self, event):
        id = event.get("id")
        message = event.get("message")
        username = event.get("username")
        self.send(text_data=json.dumps({
            "id": id,
            "message": message,
            "username": username
        }))
