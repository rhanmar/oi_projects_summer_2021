import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("find_me")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    "send_email_with_app_statistics": {
        "task": "send_email_with_app_statistics",
        "schedule": crontab(
            hour=7,
            minute=30,
            day_of_week=1
        ),
    },
    "send_email_with_info_about_active_meetings_around": {
        "task": "send_email_with_info_about_active_meetings_around",
        "schedule": crontab(
            hour=7,
            minute=30,
        ),
    }
}


app.autodiscover_tasks()
