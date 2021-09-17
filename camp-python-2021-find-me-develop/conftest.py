"""Configuration file for pytest
"""
from django.conf import settings

import pytest

from apps.users.factories import UserFactory
from apps.map.factories import DialogFactory, LocationFactory, MeetingFactory
from apps.users.factories import ReviewFactory
from apps.dialogs.factories import MessageFactory


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


@pytest.fixture
def user(django_db_setup, django_db_blocker):
    """Function-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = UserFactory()
        yield created_user
        created_user.delete()


@pytest.fixture
def two_users():
    """Fixture to create two users."""
    return UserFactory.create_batch(2)


@pytest.fixture
def banned_user():
    """Fixture to create a banned user."""
    return UserFactory(is_banned=True)


@pytest.fixture
def meeting(user):
    """Fixture for meeting creation."""
    return MeetingFactory(
        created_by=user,
        max_people_limit=5,
    )


@pytest.fixture
def another_user():
    """Fixture for another user."""
    return UserFactory()


@pytest.fixture
def new_meeting_data():
    """Fixture for new meeting data."""
    point = LocationFactory().point
    return {
        "title": "new_title",
        "description": "description",
        "max_people_limit": 10,
        "location_add": f"{point.x},{point.y}",
        "dialog": DialogFactory(),
    }


@pytest.fixture
def review(two_users):
    """Fixture for review creation."""
    reviewer, reviewed = two_users
    return ReviewFactory(
        reviewer=reviewer,
        reviewed=reviewed,
    )


@pytest.fixture
def dialog():
    return DialogFactory()


@pytest.fixture
def message():
    return MessageFactory()


@pytest.fixture
def auth_client(client, user):
    """Fixture of authenticated django.test.Client."""
    client.force_login(user)
    return client
