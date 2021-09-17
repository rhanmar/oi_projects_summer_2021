from django.urls import reverse

import pytest

from apps.dialogs.factories import DialogMemberFactory, MessageFactory
from apps.map.factories import MeetingFactory


@pytest.fixture(scope="module")
def meeting(django_db_setup, django_db_blocker):
    """Module-scope fixture to create meeting."""
    with django_db_blocker.unblock():
        created_meeting = MeetingFactory()
        yield created_meeting
        created_meeting.delete()


@pytest.fixture
def message(django_db_setup, django_db_blocker):
    """Module-scope fixture to create message."""
    with django_db_blocker.unblock():
        created_message = MessageFactory()
        yield created_message
        created_message.delete()


def test_can_read_dialog(meeting, user, auth_client):
    """Ensure user can read dialog only if he is a member."""
    url = reverse("v1:dialogs-detail", kwargs={"pk": meeting.dialog_id})

    resp = auth_client.get(url)
    assert resp.status_code == 403

    DialogMemberFactory(dialog=meeting.dialog, member=user)

    resp = auth_client.get(url)
    assert resp.status_code == 200


@pytest.mark.parametrize("method,status_code", [
    ("get", 200),
    ("head", 200),
    ("options", 200),
    ("put", 403),
    ("delete", 403),
    ("patch", 403),
])
def test_unsafe_methods_on_message(
    message,
    user,
    auth_client,
    method,
    status_code
):
    """Ensure that not a sender can't perform unsafe methods on message."""
    resp = auth_client.generic(
        method,
        reverse("v1:messages-detail", kwargs={"pk": message.pk}),
        data={
            "dialog": message.dialog,
            "sender": user,
            "text": "new_text",
        }
    )
    assert resp.status_code == status_code
