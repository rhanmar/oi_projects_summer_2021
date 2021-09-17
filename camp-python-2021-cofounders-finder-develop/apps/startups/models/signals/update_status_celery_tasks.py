import json
from datetime import datetime

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django_celery_beat.models import ClockedSchedule, PeriodicTask

from apps.startups.models.startups import Startup

FINISH_STARTUP_TASK = "apps.startups.celery_tasks.finish_startup"


@receiver(post_save, sender=Startup)
def setup_periodic_task(sender, instance, created, **kwargs):
    """Set up celery task for updating Startup status.

    If `end_date` has come, then Startup status will be updated to `closed`.
    """
    if created:
        # Create PeriodicTask for new Startup instance.
        clocked_schedule = ClockedSchedule.objects.create(
            clocked_time=instance.end_date
        )
        task = PeriodicTask.objects.create(
            name=f"Finish {instance.title} startup",
            task=FINISH_STARTUP_TASK,
            enabled=True,
            one_off=True,
            args=json.dumps([instance.pk]),
            clocked=clocked_schedule,
            start_time=datetime.now(),
        )
        # Using update method to avoid signals recursion.
        Startup.objects.filter(pk=instance.pk).update(update_status_task=task)
    else:
        # Update `clocked_time` if startups `end_date` was changed.
        clocked = instance.update_status_task.clocked
        if not clocked.clocked_time == instance.end_date:
            ClockedSchedule.objects.filter(pk=clocked.pk).update(
                clocked_time=instance.end_date
            )


@receiver(post_delete, sender=Startup)
def delete_periodic_task(sender, instance, **kwargs):
    """Delete related to Startup PeriodicTask and ClockedSchedule."""
    instance.update_status_task.clocked.delete()
    instance.update_status_task.delete()
