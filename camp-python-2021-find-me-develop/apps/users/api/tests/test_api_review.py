from django.urls import reverse

from rest_framework import status

import pytest

from apps.users.factories import ReviewFactory
from apps.users.models import Review


@pytest.mark.api
def test_create_review(client, two_users):
    """Test create review when authorized."""
    reviewer, reviewed = two_users
    client.force_login(reviewer)
    data = {
        "title": "new_title",
        "body": "new_body",
        "rate": 4.0,
        "reviewer": reviewer.id,
        "reviewed": reviewed.id,
    }
    response = client.post(reverse("v1:user_reviews-list"), data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1


@pytest.mark.api
def test_list_review(client, user):
    """Test list review when authorized."""
    client.force_login(user)
    response = client.get(reverse("v1:user_reviews-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.api
def test_update_review_owner(client, review):
    """Test update review when authorized."""
    reviewer = review.reviewer
    reviewed = review.reviewed
    client.force_login(reviewer)
    data = {
        "title": "changed_title",
        "body": "changed_body",
        "rate": 4.0,
        "reviewer": reviewer.id,
        "reviewed": reviewed.id,
    }
    response = client.put(
        reverse("v1:user_reviews-detail", args=[review.id]),
        data=data,
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert Review.objects.first().title == data["title"]
    assert Review.objects.first().body == data["body"]


@pytest.mark.api
def test_error_update_review_non_owner(client, user, review):
    """Test 403 on update review when non owner."""
    client.force_login(user)
    response = client.put(reverse("v1:user_reviews-detail", args=[review.id]))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_partial_update_review_owner(client, review):
    """Test partial update review when authorized."""
    reviewer = review.reviewer
    client.force_login(reviewer)
    data = {
        "title": "brand_new_title",
        "body": "brand_new_body",
    }
    response = client.patch(
        reverse("v1:user_reviews-detail", args=[review.id]),
        data=data,
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_200_OK
    assert Review.objects.first().title == data["title"]
    assert Review.objects.first().body == data["body"]


@pytest.mark.api
def test_partial_update_review_non_owner(client, user, review):
    """Test 403 on update review when non owner."""
    client.force_login(user)
    response = client.patch(
        reverse("v1:user_reviews-detail", args=[review.id])
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_delete_review_owner(client, review):
    """Test delete review when owner"""
    reviewer = review.reviewer
    client.force_login(reviewer)
    response = client.delete(
        reverse("v1:user_reviews-detail", args=[review.id])
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.api
def test_delete_review_non_owner(client, user, review):
    """Test 403 on delete review when non owner"""
    client.force_login(user)
    response = client.delete(
        reverse("v1:user_reviews-detail", args=[review.id])
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_error_create_review_non_auth(client):
    """Test 403 on create review when non owner"""
    response = client.post(reverse("v1:user_reviews-list"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_error_update_review_non_auth(client, review):
    """Test 403 on update review when non owner"""
    response = client.put(reverse("v1:user_reviews-list"), args=[review.id])
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_error_partial_update_review_non_auth(client, review):
    """Test 403 on partial update review when non owner"""
    response = client.patch(reverse("v1:user_reviews-list"), args=[review.id])
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_error_delete_review_non_auth(client, review):
    """Test 403 on delete review when non owner"""
    response = client.delete(reverse("v1:user_reviews-list"), args=[review.id])
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_to_me(client, user, two_users):
    """Test 'to_me' endpoint returns correct list."""
    auth_user = user
    for just_user in two_users:
        ReviewFactory(reviewer=just_user, reviewed=auth_user)
    client.force_login(auth_user)
    response = client.get(reverse("v1:user_reviews-to-me"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(two_users)


@pytest.mark.api
def test_to_me_error(client):
    """Test 403 on 'to_me' endpoint when non auth."""
    response = client.get(reverse("v1:user_reviews-to-me"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.api
def test_from_me(client, user, two_users):
    """Test 'from_me' endpoint returns correct list."""
    auth_user = user
    for just_user in two_users:
        ReviewFactory(reviewer=auth_user, reviewed=just_user)
    client.force_login(auth_user)
    response = client.get(reverse("v1:user_reviews-from-me"))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(two_users)


@pytest.mark.api
def test_from_me_error(client):
    """Test 403 on 'from_me' endpoint when non auth."""
    response = client.get(reverse("v1:user_reviews-from-me"))
    assert response.status_code == status.HTTP_403_FORBIDDEN
