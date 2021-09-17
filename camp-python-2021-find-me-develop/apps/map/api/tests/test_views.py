from rest_framework import status
from rest_framework.reverse import reverse

import pytest

from apps.map.factories import MeetingFactory, MeetingReviewFactory


@pytest.fixture
def review(django_db_blocker, django_db_setup):
    """Function-level fixture for review."""
    with django_db_blocker.unblock():
        new_review = MeetingReviewFactory()
        yield new_review
        new_review.delete()


def test_meeting_review_create(user, auth_client):
    """Ensure that create action works correct."""
    url = reverse("v1:review-list")
    meeting = MeetingFactory()
    data = {
        "title": "test_title",
        "body": "test_description",
        "rate": 5,
        "meeting": meeting.pk,
        "created_by": user,
    }

    resp = auth_client.post(url, data=data)
    assert resp.status_code == status.HTTP_201_CREATED

    saved_review = meeting.reviews.filter(pk=resp.data["id"])
    assert saved_review.exists()


def test_meeting_review_list(user, auth_client):
    """Ensure that list action works correct."""
    url = reverse("v1:review-list")

    resp = auth_client.get(url)
    assert resp.status_code == status.HTTP_200_OK


def test_meeting_review_retrieve(user, auth_client, review):
    """Ensure that retrieve action works correct."""
    url = reverse("v1:review-detail", kwargs={"pk": review.pk})

    resp = auth_client.get(url)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["id"] == review.pk


@pytest.mark.parametrize("self_created,status_code", [
    (False, status.HTTP_403_FORBIDDEN),
    (True, status.HTTP_200_OK),
])
def test_meeting_review_update(
    user,
    auth_client,
    review,
    self_created,
    status_code
):
    """Ensure that update and partial_update actions works correct."""
    if self_created:
        review = MeetingReviewFactory(created_by=user)

    url = reverse("v1:review-detail", kwargs={"pk": review.pk})
    data = {
        "title": "new_test_title",
        "body": "new_test_description",
        "rate": 4,
        "meeting": review.meeting.pk,
        "created_by": user.pk,
    }

    resp = auth_client.put(url, data, content_type="application/json")
    assert resp.status_code == status_code

    resp = auth_client.patch(url, data, content_type="application/json")
    assert resp.status_code == status_code


@pytest.mark.parametrize("self_created,status_code", [
    (False, status.HTTP_403_FORBIDDEN),
    (True, status.HTTP_204_NO_CONTENT),
])
def test_meeting_review_destroy(
    user,
    auth_client,
    review,
    self_created,
    status_code
):
    """Ensure that destroy action works correct."""
    if self_created:
        review = MeetingReviewFactory(created_by=user)

    url = reverse("v1:review-detail", kwargs={"pk": review.pk})

    resp = auth_client.delete(url, content_type="application/json")
    assert resp.status_code == status_code
