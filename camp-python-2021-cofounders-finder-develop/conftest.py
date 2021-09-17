"""Configuration file for pytest
"""

from django.conf import settings
from django.utils import timezone

import pytest

from apps.startups import factories as startups_factories
from apps.startups import statuses as startups_statuses
from apps.users import factories as users_factories


def pytest_configure():
    """Set up Django settings for tests.

    `pytest` automatically calls this function once when tests are run.
    """
    settings.DEBUG = False
    settings.TESTING = True

    # The default password hasher is rather slow by design.
    # https://docs.djangoproject.com/en/3.0/topics/testing/overview/
    settings.PASSWORD_HASHERS = (
        "django.contrib.auth.hashers.MD5PasswordHasher",
    )
    settings.EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # To disable celery in tests
    settings.CELERY_TASK_ALWAYS_EAGER = True


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """This hook allows all tests to access DB"""


@pytest.fixture(scope="session", autouse=True)
def temp_directory_for_media(tmpdir_factory):
    """Fixture that set temp directory for all media files.

    This fixture changes FILE_STORAGE to filesystem and provides temp dir for
    media. PyTest cleans up this temp dir by itself after few test runs
    """
    settings.DEFAULT_FILE_STORAGE = (
        "django.core.files.storage.FileSystemStorage"
    )
    media = tmpdir_factory.mktemp("tmp_media")
    settings.MEDIA_ROOT = media


@pytest.fixture(scope="module")
def user(django_db_setup, django_db_blocker):
    """Module-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = users_factories.UserFactory()
        yield created_user
        created_user.delete()


@pytest.fixture(scope="function")
def auth_client(user, client):
    """Function-level fixture for authenticated client."""
    client.force_login(user)
    return client


@pytest.fixture(scope="function")
def vacancies() -> list:
    """Create new Vacancy instances."""
    return startups_factories.VacancyFactory.create_batch(3)


@pytest.fixture(scope="function")
def startups() -> list:
    """Create new Startup instances."""
    return startups_factories.StartupFactory.create_batch(3)


@pytest.fixture(scope="function")
def open_startup():
    """Create new Startup instances with open status."""
    return startups_factories.StartupFactory.create(
        status=startups_statuses.StartupChoices.STATUS_OPEN,
        end_date=timezone.now()
    )


@pytest.fixture(scope="function")
def cvs() -> list:
    """Return batch which consists of 3 CV."""
    return users_factories.CVWith2SkillsFactory.create_batch(3)
