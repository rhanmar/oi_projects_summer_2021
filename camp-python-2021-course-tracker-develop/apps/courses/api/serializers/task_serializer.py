from rest_framework import serializers

from apps.courses import models


class TaskSerializer(serializers.ModelSerializer):
    """Serializer of Task model."""

    class Meta:
        model = models.Task
        fields = (
            "id",
            "title",
        )


class EvaluationSerializer(serializers.ModelSerializer):
    """Serializer of Evaluation model."""

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Evaluation
        fields = (
            "id",
            "comment",
            "mark",
            "owner",
            "solution",
        )


class SolutionSerializer(serializers.ModelSerializer):
    """Serializer of Solution model."""

    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Solution
        fields = (
            "id",
            "solution_description",
            "owner",
            "task",
        )
