import datetime

from celery import shared_task
from geopy import Point, distance

from libs.notifications.email import DefaultEmailNotification

from apps.map.models import Meeting
from apps.users.models import User

from .constants import DAYS_AGO, MEETING_KILOMETERS


@shared_task(name="send_email_with_app_statistics")
def send_email_with_app_statistics():
    """Send simple statistics about app to users."""
    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=DAYS_AGO)
    mails = User.objects.values_list("email", flat=True)
    users_count = User.objects.filter(
        created__gte=week_ago,
    ).count()
    meetings_count = Meeting.objects.filter(
        created__gte=week_ago,
    ).count()

    email_message = DefaultEmailNotification(
        subject="Statistics about FindMe.",
        template="email/statistics_info_message.html",
        recipient_list=mails,
        email_title="Statistics about FindMe.",
        users_count=users_count,
        meetings_count=meetings_count,
    )
    email_message.send()


@shared_task(name="send_email_with_meetings_around_for_auth_user")
def send_email_with_meetings_around_for_auth_user(
    current_location,
    current_city,
    user_id,
    user_email,
    user_first_name,
):
    """Send information about near meetings to users.

     This info based on the auth user current location.

    """
    current_user_location = Point(current_location)
    active_meetings = Meeting.objects.active_meetings().select_related(
        "location",
        "created_by",
    )
    near_meetings_counter = 0
    if active_meetings:
        for active_meeting in active_meetings:
            if active_meeting.created_by.id == user_id:
                continue
            dist = distance.great_circle(
                current_user_location,
                active_meeting.location.point,
            )
            if dist <= MEETING_KILOMETERS:
                near_meetings_counter += 1

    email_message = DefaultEmailNotification(
        subject="Meetings around your current location.",
        template="email/meetings_around_by_location_message.html",
        recipient_list=[user_email],
        email_title="Meetings around your current location.",
        meetings_count=near_meetings_counter,
        current_city=current_city,
        user_first_name=user_first_name,
    )
    email_message.send()


@shared_task(name="send_email_with_info_about_active_meetings_around")
def send_email_with_info_about_active_meetings_around():
    """Send information about near meetings to users.

    This info based on the last meeting created by every user.

    """
    users = User.objects.prefetch_related(
        "created_meetings__location",
    )
    active_meetings = Meeting.objects.active_meetings().select_related(
        "location",
    )
    for user in users:
        user_meeting = user.active_meetings.last()
        if user_meeting is not None:
            near_meetings_counter = 0
            for active_meeting in active_meetings:
                if active_meeting.location_id == user_meeting.location_id:
                    continue
                dist = distance.great_circle(
                    active_meeting.location.point,
                    user_meeting.location.point
                )
                if dist <= MEETING_KILOMETERS:
                    near_meetings_counter += 1
            email_message = DefaultEmailNotification(
                subject="Meetings around you.",
                template="email/meetings_around_periodical_message.html",
                recipient_list=[user.email],
                email_title="Meetings around you.",
                meetings_count=near_meetings_counter,
            )
            email_message.send()
