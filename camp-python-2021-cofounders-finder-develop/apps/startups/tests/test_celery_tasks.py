from django.utils import timezone

import pytest

from apps.startups.factories import StartupFactory
from apps.startups.models import Startup
from apps.startups.statuses import StartupChoices
from apps.startups.tasks import finish_startup, run_broken_startup_tasks

STATUS_FINISHED_VALUE = StartupChoices.STATUS_FINISHED.value


@pytest.fixture(scope="function")
def open_startups():
    """Create new Startup instances."""
    return StartupFactory.create_batch(
        status=StartupChoices.STATUS_OPEN,
        end_date=timezone.now(),
        size=5
    )


def test_finish_startup(open_startup):
    """Test finish_startup() task updates Startup status to finished."""
    finish_startup(open_startup.pk)
    open_startup.refresh_from_db()

    assert open_startup.status == STATUS_FINISHED_VALUE


def test_run_broken_startup_tasks(open_startups):
    """Test run_broken_startup_tasks() runs tasks."""
    run_broken_startup_tasks()
    startups_pks = list(map(lambda x: x.pk, open_startups))
    updated_startups = Startup.objects.filter(pk__in=startups_pks)
    filtered_startups = updated_startups.filter(status=STATUS_FINISHED_VALUE)
    assert len(open_startups) == filtered_startups.count()
