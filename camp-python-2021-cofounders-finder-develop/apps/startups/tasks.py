from django.utils import timezone

from celery import group, shared_task

from . import models
from .statuses import StartupChoices


@shared_task
def finish_startup(startup_pk: int):
    """Update Startup status to closed by its primary key.
    Celery shared task.

    Params:
        pk (int): primary key of Startup instance.
    """
    models.Startup.objects.filter(pk=startup_pk).update(
        status=StartupChoices.STATUS_FINISHED
    )


@shared_task(name="run_broken_startup_tasks")
def run_broken_startup_tasks():
    """Run `finish_startup` tasks, which were not run for some reasons before.
    Celery shared task.
    """
    now = timezone.now()
    startups_pks = models.Startup.objects.filter(
        end_date__lt=now,
        status__in=[
            StartupChoices.STATUS_OPEN,
            StartupChoices.STATUS_IN_PROGRESS
        ],
    ).values_list("pk", flat=True)

    tasks_group = group(finish_startup.signature(pk) for pk in startups_pks)
    tasks_group.apply_async()
