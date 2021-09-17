import json

from django.contrib.contenttypes.models import ContentType

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.courses.forms import AddCommentForm


class CommentsConsumer(AsyncWebsocketConsumer):
    """Consumer for add comments."""

    def serialize_comment(self, user, comment):
        """Convert instance of Comment to json.

        Args:
            user (User): instance of user who added comment.
            comment (Comment): instance of created comment.

        Returns:
            str: serialized to json instance of Comment.

        """
        comment_data = {
            "status": "success",
            "id": comment.id,
            "text": comment.text,
            "username": user.get_full_name(),
            "user_avatar": user.profile_image_thumbnail.url,
            "time": comment.created_at.strftime("%b. %d, %Y, %H:%M %p"),
            "parent": comment.parent_id,
        }
        return json.dumps(comment_data)

    async def receive(self, text_data=None, bytes_data=None):
        """Receive new comment text and parent, return created comment."""
        parsed_text_data = json.loads(text_data)
        user = self.scope["user"]
        content_type = await self.get_content_type()
        object_id = int(self.scope["url_route"]["kwargs"]["pk"])

        result = await self.save_comment(
            object_id,
            content_type,
            user,
            parsed_text_data
        )

        await self.send(result)

    @database_sync_to_async
    def get_content_type(self):
        """Return instance of ContentType by model name.

        Returns:
            ContentType: content type of model which comment is attached.

        """
        model_name = self.scope["url_route"]["kwargs"]["model_name"]
        return ContentType.objects.get(model=model_name)

    @database_sync_to_async
    def save_comment(self, object_id, content_type, user, text_data):
        """Create new comment and return it or return failed message.

        Args:
            object_id (int): id what the comment is attached to.
            content_type (ContentType): model which comment is attached.
            user (User): who leaves the comment.
            text_data (dict): dict with text and parent id.

        Returns:
            str: serialized to json response.

        """
        form = AddCommentForm(content_type, data={"text": text_data["text"]})
        form.instance.object_id = object_id
        form.instance.user_id = user.id

        if text_data["parent"]:
            form.instance.parent_id = int(text_data["parent"])

        if form.is_valid():
            comment = form.save()
            return self.serialize_comment(user, comment)
        return json.dumps({"status": "failed", "errors": form.errors})


class NotificationConsumer(AsyncWebsocketConsumer):
    """Async consumer to handle notification logic."""

    async def connect(self):
        """Handle websocket connection asynchronously.

        Add current user to group by his id. This is done for user take only
        notification about self solutions, not everyone.
        """
        user_id = self.scope["url_route"]["kwargs"]["token"]
        user_group_name = f"user_{user_id}"

        await self.channel_layer.group_add(
            user_group_name,
            self.channel_name,
        )

        await self.accept()

    async def notification_message(self, event):
        """Receive new message event and send it to websocket."""
        task_title = event["task_title"]
        user = event["user_id"]
        evaluator = event["evaluator"]

        await self.send(text_data=json.dumps({
            "task_title": task_title,
            "user_id": str(user),
            "evaluator": evaluator,
        }))
