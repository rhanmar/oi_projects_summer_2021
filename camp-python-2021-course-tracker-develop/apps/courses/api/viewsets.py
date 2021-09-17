from django.db.models import Prefetch

from rest_framework import mixins

from apps.courses import models
from apps.courses.models.tasks import Task

from ...core.api.views import BaseViewSet, CRUDViewSet
from . import serializers
from .permissions import IsMentor, IsOwnerSelf


class TopicViewSet(mixins.ListModelMixin,
                   BaseViewSet):
    """Represent list only Topic ViewSet."""

    queryset = models.Topic.objects.prefetch_related(
        Prefetch("tasks", Task.objects.not_hidden()),
        Prefetch("speaker"),
        Prefetch("tags")
    )
    serializer_class = serializers.TopicSerializer
    filterset_fields = (
        "chapter",
        "tags",
        "speaker",
        "title",
        "description",
    )


class EvaluationViewSet(CRUDViewSet):
    """Represent CRUD Evaluations ViewSet."""
    queryset = models.Evaluation.objects.select_related(
        "solution",
        "owner"
    )
    serializer_class = serializers.EvaluationSerializer
    permission_classes = [IsMentor, IsOwnerSelf]
    filterset_fields = (
        "owner",
        "solution",
    )


class SolutionViewSet(CRUDViewSet):
    """Represent CRUD solutions ViewSet."""
    queryset = models.Solution.objects.select_related(
        "task",
        "owner",
    ).prefetch_related("evaluated_solution")
    serializer_class = serializers.SolutionSerializer
    permission_classes = [IsOwnerSelf]
    filterset_fields = (
        "owner",
        "task",
    )
