from django.conf import settings

from libs.notifications.email import DefaultEmailNotification


def email_sender(**kwargs):
    """Function which send any email."""
    email_message = DefaultEmailNotification(
        app_url=settings.FRONTEND_URL,
        app_label=settings.APP_LABEL,
        **kwargs,
    )
    email_message.send()
