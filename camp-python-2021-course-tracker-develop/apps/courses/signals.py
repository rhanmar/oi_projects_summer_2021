from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.courses.models import Evaluation

__all__ = (
    "notify_user_about_new_evaluation",
)


# pylint: disable=unused-argument
# sender and **kwargs it is required arguments for signal
@receiver(post_save, sender=Evaluation)
def notify_user_about_new_evaluation(
    sender: Evaluation,
    instance: Evaluation,
    **kwargs,
):
    """Send a notification to owner of solution after create a evaluation.

    Args:
        sender: Evaluation model class.
        instance: instance of class.
        **kwargs: any keyword arguments.
    """
    channel_layer = get_channel_layer()
    solution = instance.solution
    evaluator = str(instance.owner)
    user_pk = solution.owner.pk

    async_to_sync(channel_layer.group_send)(
        f"user_{user_pk}",
        {
            "type": "notification_message",
            "task_title": solution.task.title,
            "evaluator": evaluator,
            "user_id": user_pk,
        }
    )
