from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StartupChoices(TextChoices):
    """Status text choices of Startup.

    ACTIVE_STATUSES (tuple): Statuses that represent active state of Startup.

    Statuses:
        STATUS_OPEN: "open",
        STATUS_IN_PROGRESS: "in progress",
        STATUS_FINISHED: "finished",
        STATUS_CLOSED: "closed",
        STATUS_ARCHIVED: "archived"
    """
    STATUS_OPEN = "open", _("Open")
    STATUS_IN_PROGRESS = "in progress", _("In progress")
    STATUS_FINISHED = "finished", _("Finished")
    STATUS_CLOSED = "closed", _("Closed")
    STATUS_ARCHIVED = "archived", _("In Archive")


class RequestChoices(TextChoices):
    """Status text choices of Request.

    Statuses:
        STATUS_UNDER_CONSIDERATION: "open",
        STATUS_REJECTED: "in progress",
        STATUS_ARCHIVED: "archived"
    """

    STATUS_UNDER_CONSIDERATION = "open", _("Under Consideration")
    STATUS_REJECTED = "in progress", _("Rejected")
    STATUS_ARCHIVED = "archived", _("In archive")


class VacancyChoices(TextChoices):
    """Status text choices of Vacancy.

    Statuses:
        STATUS_OPEN: "open",
        STATUS_CLOSED: "closed",
        STATUS_ARCHIVED: "archived"
    """

    STATUS_OPEN = "open", _("Open")
    STATUS_CLOSED = "closed", _("Closed")
    STATUS_ARCHIVED = "archived", _("In Archive")
