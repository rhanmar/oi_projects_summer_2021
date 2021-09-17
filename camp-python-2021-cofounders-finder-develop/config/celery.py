import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("cofounders_finder")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "run_broken_startup_status_tasks": {
        "task": "run_broken_startup_tasks",
        "schedule": crontab(hour="*/2")
    },
    "delete_inactive_users": {
        "task": "delete_inactive_users",
        "schedule": crontab(hour="*/1")
    }
}
