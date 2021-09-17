from django.urls import reverse

import pytest

from apps.users.factories import ReviewFactory


@pytest.mark.parametrize(
    "link, has_pk",
    [
        ("top_users", False),
        ("main_page", False),
        ("user_reviews", True),
        ("user_edit", False),
        ("user_profile", True),
    ]
)
def test_redirect_non_auth_user(client, user, link, has_pk):
    """Test redirect to login when unauthorized user goes to link."""
    if has_pk:
        link = reverse(link, args=[user.pk])
    else:
        link = reverse(link)
    response = client.get(link)
    assert response.status_code == 302
    assert response.url.split("?next")[0] == reverse("login")


@pytest.mark.parametrize(
    "link, has_pk",
    [
        ("top_users", False),
        ("main_page", False),
        ("user_reviews", True),
        ("user_edit", False),
        ("user_profile", True),
    ]
)
def test_auth_user(client, user, link, has_pk):
    """Test that authorized user goes to link successfully."""
    if has_pk:
        link = reverse(link, args=[user.pk])
    else:
        link = reverse(link)
    client.force_login(user)
    response = client.get(link)
    assert response.status_code == 200
    assert response.request["PATH_INFO"] == link


@pytest.mark.parametrize(
    "link, has_pk",
    [
        ("top_users", False),
        ("main_page", False),
        ("user_reviews", True),
        ("user_edit", False),
        ("user_profile", True),
    ]
)
def test_banned_user(client, banned_user, link, has_pk):
    """Test that banned user is redirected to ban page."""
    if has_pk:
        link = reverse(link, args=[banned_user.pk])
    else:
        link = reverse(link)
    client.force_login(banned_user)
    response = client.get(link)
    assert response.status_code == 302
    assert response.url.split("?next")[0] == reverse("ban_page")


def test_user_profile_not_valid(client, user):
    """Test exception is raised when get non existent user profile."""
    client.force_login(user)
    response = client.get(reverse("user_profile", args=[0]))
    assert response.status_code == 403


def test_error_give_review_twice(client, two_users):
    """Test error when user tries to give a review to the same user twice."""
    auth_user, just_user = two_users
    ReviewFactory(reviewer=auth_user, reviewed=just_user)
    client.force_login(auth_user)
    response = client.post(reverse("user_add_review", args=[just_user.id]))
    response_error = response.context["form"].errors["__all__"][0]
    assert response_error == "You can't give a review to the same user twice."


def test_error_give_review_to_himself(client, user):
    """Test error when user tries to give a review to himself."""
    client.force_login(user)
    response = client.post(reverse("user_add_review", args=[user.id]))
    response_error = response.context["form"].errors["__all__"][0]
    assert response_error == "You cannot add review for yourself."
