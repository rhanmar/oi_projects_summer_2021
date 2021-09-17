from django.contrib.auth import get_user_model
from django.utils import timezone

from celery.app import shared_task

user_model = get_user_model()


@shared_task(name="delete_inactive_users")
def delete_inactive_users():
    """Delete inactive users that created later than 24 hours."""
    time_threshold = timezone.now() - timezone.timedelta(hours=24)
    users = user_model.objects.filter(
        is_active=False,
        created__lt=time_threshold,
    )
    users.delete()
