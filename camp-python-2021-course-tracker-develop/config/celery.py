import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("course_tracker")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "send_email_task_without_solution_notification": {
        "task": "send_email_task_without_solution_notification",
        "schedule": crontab(
            hour=8,
            day_of_week='mon,tue,wed,thu,fri',
        ),
    }
}

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_email_with_topic_notification": {
        "task": "send_email_with_topic_notification",
        "schedule": crontab(
            hour=8,
            day_of_week='mon,tue,wed,thu,fri',
        ),
    }
}

app.conf.beat_schedule = {
    "fill_topics_by_default_speakers": {
        "task": "fill_topics_by_default_speakers",
        "schedule": crontab(minute=0, hour=0),
    }
}

