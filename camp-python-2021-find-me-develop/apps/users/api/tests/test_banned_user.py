from django.urls import reverse

from rest_framework import status

import pytest
from pytest_lazyfixture import lazy_fixture

METHODS = [
    "get",
    "post",
    "put",
    "patch",
    "delete",
]


@pytest.mark.parametrize("path", [
    "v1:user_reviews-list",
    "v1:users-list",
    "v1:dialogs-list",
    "v1:messages-list",
    "v1:location-list",
    "v1:meeting-list",
    "v1:user_reviews-from-me",
    "v1:user_reviews-to-me",
])
def test_errors_for_banned_user_on_urls_without_pk(client, banned_user, path):
    client.force_login(banned_user)
    for method in METHODS:
        response = client.generic(method, reverse(path))
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("path,fixture", [
    ("v1:user_reviews-detail", lazy_fixture("review")),
    ("v1:users-detail", lazy_fixture("user")),
    ("v1:users-join", lazy_fixture("user")),
    ("v1:dialogs-detail", lazy_fixture("dialog")),
    ("v1:messages-detail", lazy_fixture("message")),
    ("v1:meeting-detail", lazy_fixture("meeting")),
    ("v1:meeting-join", lazy_fixture("meeting")),
])
def test_errors_for_banned_user_on_urls_with_pk(
    client,
    banned_user,
    path,
    fixture
):
    obj = fixture
    client.force_login(banned_user)
    for method in METHODS:
        response = client.generic(method, reverse(path, args=[obj.pk]))
        assert response.status_code == status.HTTP_403_FORBIDDEN
