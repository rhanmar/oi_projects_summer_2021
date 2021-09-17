from django.urls import reverse_lazy

import pytest


@pytest.mark.parametrize("test_data", [
    {
        "github_username": "new_github_username",
        "links-TOTAL_FORMS": 0,
        "links-INITIAL_FORMS": 0,
        "links-MIN_NUM_FORMS": 0,
        "links-MAX_NUM_FORMS": 1000,
    },
    {
        "first_name": "test",
        "github_username": "other_github_username",
        "links-TOTAL_FORMS": 0,
        "links-INITIAL_FORMS": 0,
        "links-MIN_NUM_FORMS": 0,
        "links-MAX_NUM_FORMS": 1000,
    },
    {
        "first_name": "",
        "github_username": "other_github_username",
        "links-TOTAL_FORMS": 0,
        "links-INITIAL_FORMS": 0,
        "links-MIN_NUM_FORMS": 0,
        "links-MAX_NUM_FORMS": 1000,
    },
])
def test_user_profile_change_correct(auth_user, client, test_data):
    """Ensure that you can change user fields correctly."""
    response = client.post(
        reverse_lazy("profile-update"),
        data=test_data
    )
    auth_user.refresh_from_db()
    assert response.status_code == 302
    assert auth_user.github_username == test_data["github_username"]


@pytest.mark.parametrize("test_data, expected", [
    (
        {
            "github_username": "new_github_username",
            "links-TOTAL_FORMS": 1,
            "links-INITIAL_FORMS": 0,
            "links-MIN_NUM_FORMS": 0,
            "links-MAX_NUM_FORMS": 1000,
            "links-0-title": "test link",
            "links-0-url": "http://testslug.com/",
        },
        1
    ),
    (
        {
            "github_username": "new_github_username",
            "links-TOTAL_FORMS": 2,
            "links-INITIAL_FORMS": 0,
            "links-MIN_NUM_FORMS": 0,
            "links-MAX_NUM_FORMS": 1000,
            "links-0-title": "test link 1",
            "links-0-url": "http://testslug1.com/",
            "links-1-title": "test link 2",
            "links-1-url": "http://testslug2.com/",
        },
        2
    ),
])
def test_userlinks_change_correct(auth_user, client, test_data, expected):
    """Ensure that you can change user links correctly."""
    response = client.post(
        reverse_lazy("profile-update"),
        data=test_data,
        follow=True,
    )
    auth_user.refresh_from_db()
    assert response.status_code == 200
    assert auth_user.links.count() == expected
