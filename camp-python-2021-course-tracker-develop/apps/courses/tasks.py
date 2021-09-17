from datetime import date, timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from celery import shared_task

from libs.notifications.email import DefaultEmailNotification

from apps.courses.constants import (
    COUNT_DAYS_FOR_NOTIFICATION,
    MAX_DAYS_FOR_BECOME_MENTOR,
)
from apps.courses.models import Task, Topic
from apps.courses.services import email_sender
from apps.users.models import User


@shared_task(name="send_email_with_topic_notification")
def send_email_with_topic_notification():
    """Check all topics and send email if one days remaining.

    Email will send for all members of current course in weekdays.
    """
    topics = Topic.objects.all().prefetch_related("chapter__course")
    now_date = date.today()
    max_timedelta = COUNT_DAYS_FOR_NOTIFICATION
    for topic in topics:
        if topic.reading_date - now_date > max_timedelta:
            continue
        course = topic.chapter.course
        course_users = course.users.all()
        to_emails = [str(user.email) for user in course_users]
        mail_subject = _("Notification about new topic")
        email_message = DefaultEmailNotification(
            subject=mail_subject,
            recipient_list=to_emails,
            template="users/emails/topic_notification.html",
            topic_name=topic.title,
            topic_id=topic.id,
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
        )
        email_message.send()


@shared_task
def fill_topics_by_default_speakers():
    """Check all topics and set default speaker if five days remaining."""
    topics = Topic.objects.all().prefetch_related("chapter__course")
    current_date = timezone.now().date()
    max_timedelta = timedelta(days=MAX_DAYS_FOR_BECOME_MENTOR)
    for topic in topics:
        if (topic.speaker
                or topic.reading_date - current_date > max_timedelta):
            continue
        course = topic.chapter.course
        topic.speaker = course.default_speaker


@shared_task(name="send_email_task_without_solution_notification")
def send_email_task_without_solution_notification():
    """Check all tasks and send email if its remaining.

    Email will send in weekdays for all members of any course which have any
    overdue task without solution .
    """
    now_date = date.today()
    tasks = Task.objects.filter(topic__reading_date__lt=now_date)
    users = User.objects.all()
    for user in users:
        tasks_without_solution = tasks.exclude(solution=user)
        to_email = [user.email]
        mail_subject = _("Notification about new Task")
        email_sender(
            subject=mail_subject,
            recipient_list=to_email,
            template="users/emails/task_notification.html",
            tasks=tasks_without_solution,
        )
