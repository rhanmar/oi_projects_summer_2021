from django.urls import reverse

from rest_framework import status

from apps.map.factories import MeetingFactory


def test_locations_list_for_user_in_blacklist(client, two_users):
    """Test that user doesn't see meetings from users who banned him."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    client.post(reverse("user_blacklist_add", args=[just_user.id]))
    MeetingFactory(created_by=auth_user)
    client.logout()

    client.force_login(just_user)
    response = client.get(reverse("v1:location-list"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


def test_join_error_for_user_in_blacklist(client, two_users):
    """Test that user in blacklist can't join to the meeting."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    client.post(reverse("user_blacklist_add", args=[just_user.id]))
    meeting = MeetingFactory(created_by=auth_user)
    client.logout()

    client.force_login(just_user)
    response = client.post(reverse("v1:meeting-join", args=[meeting.pk]))
    assert response.status_code == status.HTTP_403_FORBIDDEN
