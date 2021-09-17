from django.urls import reverse

import pytest
from pytest_django.asserts import assertTemplateUsed

from apps.users.factories import ReviewFactory
from apps.users.models import BlackList


def test_blacklist_add(client, two_users):
    """Test that auth user can add other user to his blacklist."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    response = client.post(reverse("user_blacklist_add", args=[just_user.id]))
    assert response.status_code == 302
    assert auth_user.banned.filter(
        banned_user_id=just_user.id
    ).first().banned_user.id == just_user.id
    assert just_user.banned_by.filter(
        user_id=auth_user.id
    ).first().user.id == auth_user.id


def test_blacklist_remove(client, two_users):
    """Test that auth user can remove other user from his blacklist."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    _ = client.post(reverse("user_blacklist_add", args=[just_user.id]))
    blacklist_item = BlackList.objects.first()
    response = client.post(reverse("user_blacklist_remove", args=[
        blacklist_item.id
    ]))
    assert response.status_code == 302
    assert len(auth_user.banned.all()) == 0
    assert len(just_user.banned_by.all()) == 0


def test_blacklist_remove_not_valid_key(client, two_users):
    """Test exception is raised when remove non existent blacklist item."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    _ = client.post(reverse("user_blacklist_add", args=[just_user.id]))
    response = client.post(reverse("user_blacklist_remove", args=[0]))
    assert response.status_code == 403


def test_blacklist_show(client, two_users, user):
    """Test that user has correct blacklist."""
    auth_user, just_user1 = two_users
    just_user2 = user
    client.force_login(auth_user)
    _ = client.post(reverse("user_blacklist_add", args=[just_user1.id]))
    _ = client.post(reverse("user_blacklist_add", args=[just_user2.id]))
    response = client.get(reverse("user_blacklist"))
    assert response.status_code == 200
    assert len(response.context["blacklist"]) == 2
    assert (auth_user.banned.all().first().id
            == response.context["blacklist"].first().id)


def test_blacklist_error_self_profile(client, user):
    """Test exception is raised when user tries to add himself to blacklist."""
    client.force_login(user)
    response = client.post(reverse("user_blacklist_add", args=[user.id]))
    assert response.status_code == 403


def test_blacklist_error_double_add_error(client, two_users):
    """Test exception is raised when user is added to blacklist two times."""
    auth_user, just_user = two_users
    client.force_login(auth_user)
    _ = client.post(reverse("user_blacklist_add", args=[just_user.id]))
    response = client.post(reverse("user_blacklist_add", args=[just_user.id]))
    assert response.status_code == 403


def test_blacklist_add_non_existent_user_error(client, user):
    """Test exception is raised when unexistent user is added to blacklist."""
    client.force_login(user)
    response = client.post(reverse("user_blacklist_add", args=[404]))
    assert response.status_code == 403


def test_blacklist_add_redirect_when_non_auth(client, user):
    """Test redirect to login when non auth wants to add to blacklist."""
    response = client.post(reverse("user_blacklist_add", args=[user.id]))
    assert response.url.split("?next")[0] == reverse("login")


def test_blacklist_remove_redirect_when_non_auth(client, user):
    """Test redirect to login when non auth wants to remove from blacklist."""
    response = client.post(reverse("user_blacklist_remove", args=[user.id]))
    assert response.url.split("?next")[0] == reverse("login")


def test_blacklist_show_redirect_when_non_auth(client):
    """Test redirect to login when non auth wants to get blacklist."""
    response = client.post(reverse("user_blacklist"))
    assert response.url.split("?next")[0] == reverse("login")


@pytest.mark.parametrize(
    "link, has_user_id",
    [
        ("user_reviews", True),
        ("user_profile", True),
        ("user_add_review", True),
        ("user_add_report", True),
    ]
)
def test_blacklist_mixin_open_right_template(
    client,
    two_users,
    link,
    has_user_id
):
    """Test redirect to blacklist_message.html when user in blacklist."""
    who_bans, who_is_banned = two_users
    client.force_login(who_bans)
    if has_user_id:
        link = reverse(link, args=[who_bans.pk])
    else:
        link = reverse(link)
    _ = client.post(reverse("user_blacklist_add", args=[who_is_banned.id]))
    client.logout()
    client.force_login(who_is_banned)
    response = client.get(link)
    assertTemplateUsed(response, "users/blacklist_message.html")


@pytest.mark.parametrize(
    "link",
    [
        "user_edit_review",
        "user_detail_review",
        "user_delete_review",
    ]
)
def test_blacklist_mixin_with_edit_detail_delete_review(
    client,
    two_users,
    link
):
    """Test redirect to blacklist_message.html when user in blacklist."""
    who_bans, who_is_banned = two_users
    review = ReviewFactory(reviewer=who_is_banned, reviewed=who_bans)
    client.force_login(who_bans)
    _ = client.post(reverse("user_blacklist_add", args=[who_is_banned.id]))
    client.logout()
    client.force_login(who_is_banned)
    response = client.post(reverse(link, args=[who_bans.id, review.id]))
    assertTemplateUsed(response, "users/blacklist_message.html")
