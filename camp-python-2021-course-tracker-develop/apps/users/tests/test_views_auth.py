from django.test import Client
from django.urls import reverse_lazy

import pytest

from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture
def set_up_test_client():
    """Set up client instance."""
    # pylint: disable=attribute-defined-outside-init
    client = Client()
    return client


@pytest.fixture
def create_test_users():
    """Create some test users with UserFactory."""
    users = UserFactory.create_batch(5)
    return users


@pytest.fixture
def signup_users(set_up_test_client, create_test_users):
    """Fixture to register test users.

    Args:
        set_up_test_client: prepare client to perform requests.
        create_test_users: prepare users.
    """
    users = create_test_users
    client = set_up_test_client
    for user in users:
        response = client.post(
            reverse_lazy("signup"),
            data={
                "email": user.email,
                "password1": "123",
                "password2": "123"
            }
        )
        assert response.status_code == 200
    return users


def test_user_signup(signup_users):
    """Test that user can sign up correctly.

    Args:
        signup_users: fixture to register test users.
    """
    for user in signup_users:
        registered_user = User.objects.get(email=user.email)
        assert user == registered_user


def test_user_login(signup_users, set_up_test_client):
    """Test that user can log in correctly.

    Args:
        signup_users: fixture to register test users.
    """
    client = set_up_test_client
    for user in signup_users:
        user.set_password("123")
        user.is_active = True
        user.save()
        can_login = client.login(email=user.email, password="123")
        assert can_login
