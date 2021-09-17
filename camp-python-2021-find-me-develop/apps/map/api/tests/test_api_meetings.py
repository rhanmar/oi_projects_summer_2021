from datetime import timedelta

from django.urls import reverse

from rest_framework import status

import pytest

from apps.map.factories import DialogFactory, LocationFactory, MeetingFactory
from apps.map.models import Meeting
from apps.users.factories import BlackListFactory


@pytest.mark.api_meetings
def test_create_meeting(client, user, new_meeting_data):
    """Test create review when authorized."""
    client.force_login(user)
    response = client.post(reverse("v1:meeting-list"), data=new_meeting_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Meeting.objects.count() == 1


@pytest.mark.api_meetings
def test_create_meeting_non_auth(client):
    """Test 403 error on create meeting when non auth."""
    response = client.post(reverse("v1:meeting-list"), data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_create_meeting_not_valid_data(client, user):
    """Test 400 error on create meeting with not valid data."""
    client.force_login(user)
    point = LocationFactory().point
    data = {
        "description": "description",
        "max_people_limit": 10,
        "location_add": f"{point.x},{point.y}",
        "dialog": DialogFactory(),
    }
    response = client.post(reverse("v1:meeting-list"), data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Meeting.objects.count() == 0


@pytest.mark.api_meetings
def test_update_meeting(client, meeting):
    """Test update review when authorized."""
    meeting_owner = meeting.created_by
    client.force_login(meeting_owner)
    point = LocationFactory().point
    data = {
        "title": "brand new title",
        "description": "description",
        "max_people_limit": 10,
        "location_add": f"{point.x},{point.y}",
        "deadline": meeting.deadline + timedelta(hours=1),
        "created_by": meeting_owner.id
    }
    response = client.put(
        reverse("v1:meeting-detail", args=[meeting.pk]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert Meeting.objects.count() == 1
    assert Meeting.objects.first().title == data["title"]


@pytest.mark.api_meetings
def test_update_meeting_not_valid_data(client, meeting):
    """Test 400 error update review when not valid data."""
    meeting_owner = meeting.created_by
    client.force_login(meeting_owner)
    point = LocationFactory().point
    data = {
        "title": "",
        "description": "description",
        "max_people_limit": 10,
        "location_add": f"{point.x},{point.y}",
        "deadline": meeting.deadline + timedelta(hours=1),
        "created_by": meeting_owner.id
    }
    response = client.put(
        reverse("v1:meeting-detail", args=[meeting.pk]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Meeting.objects.first().title != data["title"]


@pytest.mark.api_meetings
def test_update_meeting_non_auth(client):
    """Test 403 error on update meeting when non auth."""
    meeting = MeetingFactory()
    response = client.put(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_update_meeting_non_owner(client, meeting, another_user):
    """Test 403 error on update meeting when non owner."""
    client.force_login(another_user)
    response = client.put(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_partial_update_meeting(client, meeting):
    """Test partial update meeting when auth."""
    meeting_owner = meeting.created_by
    client.force_login(meeting_owner)
    data = {
        "title": "brand new title",
    }
    response = client.patch(
        reverse("v1:meeting-detail", args=[meeting.pk]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert Meeting.objects.first().title == data["title"]


@pytest.mark.api_meetings
def test_partial_update_meeting_not_valid_data(client, meeting):
    """Test 400 error on partial update meeting when not valid data."""
    meeting_owner = meeting.created_by
    client.force_login(meeting_owner)
    data = {
        "title": "",
    }
    response = client.patch(
        reverse("v1:meeting-detail", args=[meeting.pk]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Meeting.objects.first().title != data["title"]


@pytest.mark.api_meetings
def test_partial_update_meeting_non_auth(client, meeting):
    """Test 403 error on patrial update meeting when non auth."""
    response = client.patch(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_partial_update_meeting_non_owner(client, meeting, another_user):
    """Test 403 error on patrial update meeting when non owner."""
    client.force_login(another_user)
    response = client.patch(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_delete_meeting(client, meeting):
    """Test delete meeting."""
    client.force_login(meeting.created_by)
    response = client.delete(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.api_meetings
def test_delete_meeting_non_auth(client, meeting):
    """Test 403 error on delete meeting when non auth."""
    response = client.delete(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_delete_meeting_non_owner(client, meeting, another_user):
    """Test 403 error on delete meeting when non owner."""
    client.force_login(another_user)
    response = client.delete(
        reverse("v1:meeting-detail", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_join_meeting(client, meeting, another_user):
    """Test join meeting."""
    client.force_login(another_user)
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.api_meetings
def test_join_meeting_non_auth(client, meeting):
    """Test 403 error on join meeting when non auth."""
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_join_meeting_banned(client, meeting, banned_user):
    """Test 403 error on join meeting when banned."""
    client.force_login(banned_user)
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_join_meeting_blacklisted(client, meeting, another_user):
    """Test 403 error on join meeting when in meeting owner's blacklist."""
    meeting_owner = meeting.created_by
    BlackListFactory(user=meeting_owner, banned_user=another_user)
    client.force_login(another_user)
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.pk]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_join_meeting_when_full(client, user, another_user, new_meeting_data):
    """Test 403 error on join meeting when meeting is full."""
    new_meeting_data["max_people_limit"] = 1
    client.force_login(user)
    client.post(reverse("v1:meeting-list"), data=new_meeting_data)
    client.logout()

    client.force_login(another_user)
    meeting_id = Meeting.objects.first().id
    response = client.post(
        reverse("v1:meeting-join", args=[meeting_id]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api_meetings
def test_join_own_meeting(client, meeting):
    """Test 403 error on join meeting when meeting is full."""
    client.force_login(meeting.created_by)
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.id]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("value", [
    -1,
    0,
    2.4,
    "test",
])
def test_create_meeting_not_valid_max_people_limit(
    client,
    user,
    new_meeting_data,
    value
):
    """Test create meeting with not valid 'max_people_limit'."""
    new_meeting_data["max_people_limit"] = value
    client.force_login(user)
    response = client.post(reverse("v1:meeting-list"), data=new_meeting_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.api_meetings
@pytest.mark.parametrize("value", [
    -1,
    0,
    2.4,
])
def test_update_meeting_not_valid_max_people_limit(client, meeting, value):
    """Test create meeting with not valid 'max_people_limit'."""
    meeting_owner = meeting.created_by
    client.force_login(meeting_owner)
    point = LocationFactory().point
    data = {
        "title": "new_title",
        "description": "description",
        "max_people_limit": value,
        "location_add": f"{point.x},{point.y}",
        "deadline": meeting.deadline + timedelta(hours=1),
        "created_by": meeting_owner.id
    }
    response = client.put(
        reverse("v1:meeting-detail", args=[meeting.pk]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Meeting.objects.first().title != data["title"]


@pytest.mark.ban
def test_join_banned_user(client, banned_user, meeting):
    """Test that banned user is not able to join to any meeting."""
    client.force_login(banned_user)
    response = client.post(
        reverse("v1:meeting-join", args=[meeting.id]),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
