import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.dialogs.api.serializers import DialogMessageSerializer
from apps.dialogs.models import Dialog


@database_sync_to_async
def get_user_dialogs(user):
    """Fetch all user's dialogs."""
    return user.dialog_membership.select_related("dialog")


@database_sync_to_async
def get_dialog_title(dialog_id):
    """Fetch dialog's title."""
    return Dialog.objects.get(pk=dialog_id).title


class DialogNotificationConsumer(AsyncWebsocketConsumer):
    """Async consumer to handle notifications."""

    notification_group_name = "dialog_notifications"

    async def connect(self):
        """Handle websocket connection asynchronously."""
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        """Handle websocket disconnect asynchronously."""
        # pylint:disable=unused-argument
        await self.channel_layer.group_discard(
            self.notification_group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        """Send notification about new message to all group members."""
        user = self.scope["user"]
        dialog_id = int(event["dialog_id"])
        message = event["message"]
        sender = event["sender"]
        user_dialogs = await get_user_dialogs(user)

        is_user_in_dialog = await database_sync_to_async(
            user_dialogs.filter(
                dialog_id=dialog_id
            ).exists)()

        if is_user_in_dialog and sender != user.pk:
            dialog_title = await get_dialog_title(dialog_id)

            await self.send(
                text_data=json.dumps({
                    "message": message,
                    "sender": str(sender),
                    "title": dialog_title,
                    "dialog": dialog_id,
                })
            )


class ChatConsumer(AsyncWebsocketConsumer):
    """Async consumer to handle chat logic."""

    notification_class = DialogNotificationConsumer

    async def connect(self):
        """Handle websocket connection asynchronously."""
        # pylint:disable=attribute-defined-outside-init
        self.dialog_id = self.scope["url_route"]["kwargs"]["dialog_id"]
        self.dialog_group_name = f"chat_{self.dialog_id}"

        user_dialogs = await get_user_dialogs(self.scope["user"])
        is_user_in_dialog = await database_sync_to_async(
            user_dialogs.filter(
                dialog_id=self.dialog_id
            ).exists)()

        if not is_user_in_dialog:
            await self.close()

        await self.channel_layer.group_add(
            self.dialog_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        """Handle websocket disconnect asynchronously."""
        # pylint:disable=unused-argument
        await self.channel_layer.group_discard(
            self.dialog_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """Receive new message from chat, save it to db and send to group."""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]

        message_dict = {
            "text": message,
            "sender": user.pk,
            "dialog": self.dialog_id,
        }

        await self.save_message(message_dict)

        await self.channel_layer.group_send(
            self.dialog_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": user.pk,
                "sender_data": {
                    "avatar_thumbnail": user.avatar_thumbnail.url,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            }
        )

        await self.channel_layer.group_send(
            self.notification_class.notification_group_name,
            {
                "type": "send_notification",
                "message": message,
                "sender": user.pk,
                "dialog_id": self.dialog_id
            }
        )

    @database_sync_to_async
    def save_message(self, message_dict):
        """Save message to db."""
        serializer = DialogMessageSerializer(data=message_dict)
        if serializer.is_valid():
            serializer.save()

    async def chat_message(self, event):
        """Receive new message event and send it to websocket."""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": str(event["sender"]),
            "sender_data": json.dumps(event["sender_data"]),
        }))
