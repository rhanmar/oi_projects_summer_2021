from rest_framework import serializers

from apps.courses.api.serializers import TaskSerializer
from apps.courses.models.topics import Topic


class TopicSerializer(serializers.ModelSerializer):
    """Serializer of Topic model."""

    tasks = TaskSerializer(many=True)
    speaker = serializers.StringRelatedField()

    class Meta:
        model = Topic
        fields = (
            "id",
            "chapter",
            "tags",
            "speaker",
            "title",
            "description",
            "order",
            "tasks",
        )
