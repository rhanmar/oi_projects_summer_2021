import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.models import Dialog, Message
from apps.users.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """Async consumer that accepts WebSocket connections from chat."""
    async def connect(self):
        """Accepts the WebSocket connection

        Check if user is authenticated,
        create group for current user and current connection.
        Websocket shutdown code 4401, backend_error – unauthorized.

        """
        # pylint:disable=attribute-defined-outside-init
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = str(self.user.pk)
            self.sender_email = self.user.email
            await self.channel_layer.group_add(
                self.group_name, self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=4401)

    async def disconnect(self, code):
        """Leave group on disconnect."""
        if code != 4401:
            await self.channel_layer.group_discard(
                self.group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        """Receive message from WebSocket, save it to db and send to group."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_pk = text_data_json["user_pk"]
        receiver = await self.get_user_by_pk(user_pk)
        dialog_exists = await self.dialog_exists(
            sender=self.user, recipient=receiver
        )
        await self.save_text_message(
            text=message, sender=self.user, recipient=receiver
        )
        await self.channel_layer.group_send(
            user_pk,
            {
                "type": "chat.message",
                "message": message,
                "sender": self.group_name,
                "receiver": user_pk,
                "sender_email": self.sender_email,
                "dialog_exists": dialog_exists,
            }
        )

    async def chat_message(self, event):
        """Receive message from group, send message to WebSocket."""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "receiver": event["receiver"],
            "sender_email": event["sender_email"],
            "dialog_exists": event["dialog_exists"],
        }))

    @database_sync_to_async
    def dialog_exists(self, sender, recipient):
        """Check if dialog between sender and recipient exists."""
        return Dialog.dialog_exists(sender, recipient)

    @database_sync_to_async
    def save_text_message(self, text, sender, recipient):
        """Save message to db."""
        Message.objects.create(text=text, sender=sender, recipient=recipient)

    @database_sync_to_async
    def get_user_by_pk(self, user_pk):
        """Get user from db by pk."""
        return User.objects.filter(pk=user_pk).first()
