from django.test import Client
from django.urls import reverse_lazy

import pytest


@pytest.fixture(scope="module")
def current_client():
    """Set up client instance with module scope."""
    # pylint: disable=attribute-defined-outside-init
    client = Client()
    return client


@pytest.fixture
def signed_up_user(user, current_client):
    """Sign up test user instance."""
    response = current_client.post(
        reverse_lazy("signup"),
        data={
            "email": user.email,
            "password1": "123",
            "password2": "123"
        }
    )
    assert response.status_code == 200
    return user


@pytest.fixture
def logged_in_user(signed_up_user, current_client):
    """Log in test user instance."""
    current_client.force_login(signed_up_user)
    return signed_up_user


def test_permissions_of_profile_view(current_client):
    """Test permissions of open a profile window for unauthorized users."""
    response = current_client.get(reverse_lazy("account"))
    assert response.status_code == 302


@pytest.mark.parametrize("test_data, expected", [
    (
        {
            "email": "test@test.com",
            "location": "new_name",
            "urls-TOTAL_FORMS": 1,
            "urls-INITIAL_FORMS": 0,
            "urls-MIN_NUM_FORMS": 0,
            "urls-MAX_NUM_FORMS": 1000,
            "urls-0-name": "test link",
            "urls-0-url": "test_slug",
        },
        1
    ),
    (
        {
            "email": "test@test.com",
            "urls-TOTAL_FORMS": 2,
            "urls-INITIAL_FORMS": 0,
            "urls-MIN_NUM_FORMS": 0,
            "urls-MAX_NUM_FORMS": 1000,
            "urls-0-name": "test link 1",
            "urls-0-url": "test_slug_1",
            "urls-1-name": "test link 2",
            "urls-1-url": "test_slug_2",
        },
        2
    ),
])
def test_user_links_change_correct(
    logged_in_user,
    current_client,
    test_data,
    expected
):
    """Ensure that you can change user urls correctly."""
    response = current_client.post(
        reverse_lazy("account_update"),
        data=test_data
    )
    assert response.status_code == 302
    assert logged_in_user.urls.count() == expected


@pytest.mark.parametrize("test_data", [
    {
        "location": "Krasnoyarsk",
        "email": "test@test.com",
        "urls-TOTAL_FORMS": 1,
        "urls-INITIAL_FORMS": 0,
        "urls-MIN_NUM_FORMS": 0,
        "urls-MAX_NUM_FORMS": 1000,
    },
    {
        "first_name": "test",
        "location": "test_loc",
        "email": "test@test.com",
        "urls-TOTAL_FORMS": 1,
        "urls-INITIAL_FORMS": 0,
        "urls-MIN_NUM_FORMS": 0,
        "urls-MAX_NUM_FORMS": 1000,
    },
])
def test_user_profile_change_correct(user, current_client, test_data):
    """Ensure that you can change user fields correctly."""
    current_client.force_login(user)
    response = current_client.post(
        reverse_lazy("account_update"),
        data=test_data
    )
    user.refresh_from_db()
    assert response.status_code == 302
    assert user.location == test_data["location"]


@pytest.mark.parametrize("test_data", [
    {
        "title": "test_title",
        "description": "test_description",
        "skills": [1, 2, 3],
    }
])
def test_cv_update(cvs, current_client, test_data, ):
    """Ensure that you can change cv fields correctly."""
    for curriculum_vitae in cvs:
        current_client.force_login(curriculum_vitae.owner)
        response = current_client.post(
            reverse_lazy("update_cv", kwargs={"pk": curriculum_vitae.pk}),
            data=test_data
        )
        curriculum_vitae.refresh_from_db()
        assert response.status_code == 302
        assert getattr(curriculum_vitae, "title") == test_data["title"]
