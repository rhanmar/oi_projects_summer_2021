from datetime import datetime, timedelta

from django.urls import reverse, reverse_lazy

import pytest

from apps.startups import models
from apps.users.factories import UserFactory

END_DATE = datetime.now() + timedelta(weeks=7)


@pytest.fixture
def users():
    """Create new User instances."""
    return UserFactory.create_batch(3)


def test_startups_list_view(client, startups):
    """Test that startup_list returns correct list of Startups."""
    url = reverse("startups:startups_list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["startups"].count() == len(startups)


def test_startup_detail_view(client, startups):
    """Test that startup_detail returns required startup instance."""
    url = reverse(
        "startups:startup_detail",
        kwargs={
            "pk": startups[0].pk
        }
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["startup"].title == startups[0].title
    assert response.context["startup"].text == startups[0].text


def test_startup_create_view_unauthorized(client):
    """Test a redirect when unauthorized user tries to create the startup."""
    url = reverse_lazy(
        "startups:startup_create",
    )
    response = client.get(url)
    assert response.url.split("?next")[0] == reverse_lazy("login")


def test_startup_update_view_unauthorized(client, startups):
    """Test a redirect when unauthorized user tries to update the startup."""
    url = reverse_lazy(
        "startups:startup_update",
        kwargs={
            "pk": startups[0].pk
        }
    )
    response = client.get(url)
    assert response.url.split("?next")[0] == reverse_lazy("login")


def test_startup_delete_view_unauthorized(client, startups):
    """Test a redirect when unauthorized user tries to delete the startup."""
    url = reverse_lazy(
        "startups:startup_delete",
        kwargs={
            "pk": startups[0].pk
        }
    )
    response = client.get(url)
    assert response.url.split("?next")[0] == reverse_lazy("login")


@pytest.mark.parametrize("test_data", [
    {
        "status": "open",
        "title": "startup1",
        "text": "text1",
        "end_date": END_DATE,
        "vacancies-TOTAL_FORMS": 0,
        "vacancies-INITIAL_FORMS": 0,
        "vacancies-MIN_NUM_FORMS": 0,
        "vacancies-MAX_NUM_FORMS": 1000,
    },
])
def test_startup_create_view_valid(client, users, test_data):
    """Test Startup creation with valid data."""
    user = users[0]
    client.force_login(user)
    url = reverse_lazy(
        "startups:startup_create",
    )
    response = client.post(url, data=test_data)
    new_startup = models.Startup.objects.filter(
        title=test_data["title"],
        text=test_data["text"],
    )
    assert response.status_code == 302
    assert new_startup.exists()


@pytest.mark.parametrize("test_data,errors", [
    (
        {
            "status": "open",
            "title": "startup1",
            "text": "",
            "end_date": "123",
            "vacancies-TOTAL_FORMS": 0,
            "vacancies-INITIAL_FORMS": 0,
            "vacancies-MIN_NUM_FORMS": 0,
            "vacancies-MAX_NUM_FORMS": 1000,
        },
        {
            "text": ["This field is required."],
            "end_date": ["Enter a valid date/time."],
        }
    ),
])
def test_startup_create_view_not_valid(client, users, test_data, errors):
    """Test Startup creation with invalid data."""
    user = users[0]
    client.force_login(user)
    url = reverse_lazy(
        "startups:startup_create",
    )
    response = client.post(url, data=test_data)
    assert response.status_code == 200
    assert response.context["form"].errors == errors


@pytest.mark.parametrize("test_data", [
    {
        "status": "open",
        "title": "startup1",
        "text": "text1",
        "end_date": END_DATE,
        "vacancies-TOTAL_FORMS": 0,
        "vacancies-INITIAL_FORMS": 0,
        "vacancies-MIN_NUM_FORMS": 0,
        "vacancies-MAX_NUM_FORMS": 1000,
    }
])
def test_startup_create_view_bound_with_user(client, users, test_data):
    """Test that authorized user is the owner of new startup."""
    user = users[0]
    client.force_login(user)
    url = reverse_lazy(
        "startups:startup_create",
    )
    response = client.post(url, data=test_data)
    new_startup = models.Startup.objects.filter(
        status="open",
        title="startup1",
        text="text1",
        end_date="2021-08-02",
    ).first()
    assert response.status_code == 302
    assert new_startup.owner == user


@pytest.mark.parametrize("test_data", [
    {
        "status": "open",
        "title": "startup1",
        "text": "text1",
        "end_date": END_DATE,
        "vacancies-TOTAL_FORMS": 0,
        "vacancies-INITIAL_FORMS": 0,
        "vacancies-MIN_NUM_FORMS": 0,
        "vacancies-MAX_NUM_FORMS": 1000,
    }
])
def test_startup_update_view_owner(client, startups, test_data):
    """Test Startup update by owner with valid data."""
    startup = startups[0]
    owner = startup.owner
    client.force_login(owner)
    url = reverse_lazy(
        "startups:startup_update",
        kwargs={
            "pk": startup.pk
        },
    )
    response = client.post(url, data=test_data)
    startup.refresh_from_db()
    assert response.status_code == 302
    assert startup.title == test_data["title"]
    assert startup.text == test_data["text"]


@pytest.mark.parametrize("test_data", [
    {
        "status": "open",
        "title": "startup1",
        "text": "text1",
        "end_date": END_DATE,
        "vacancies-TOTAL_FORMS": 0,
        "vacancies-INITIAL_FORMS": 0,
        "vacancies-MIN_NUM_FORMS": 0,
        "vacancies-MAX_NUM_FORMS": 1000,
    }
])
def test_startup_update_view_not_owner(client, startups, test_data):
    """Test Startup update by non-owner with valid data."""
    startup = startups[0]
    user = UserFactory()
    client.force_login(user)
    url = reverse_lazy(
        "startups:startup_update",
        kwargs={
            "pk": startup.pk
        },
    )
    response = client.post(url, data=test_data)
    startup.refresh_from_db()
    assert response.status_code == 403


@pytest.mark.parametrize("test_data,errors", [
    (
        {
            "status": "open",
            "title": "",
            "text": "",
            "end_date": END_DATE,
            "vacancies-TOTAL_FORMS": 0,
            "vacancies-INITIAL_FORMS": 0,
            "vacancies-MIN_NUM_FORMS": 0,
            "vacancies-MAX_NUM_FORMS": 1000,
        },
        {
            "title": ["This field is required."],
            "text": ["This field is required."],
        }

    ),
])
def test_startup_update_view_not_valid(client, startups, test_data, errors):
    """Test Startup update by owner with invalid data."""
    startup = startups[0]
    owner = startup.owner
    client.force_login(owner)
    url = reverse_lazy(
        "startups:startup_update",
        kwargs={
            "pk": startup.pk
        },
    )
    response = client.post(url, data=test_data)
    startup.refresh_from_db()
    assert response.context["form"].errors == errors


def test_startup_delete_view_owner(client, startups):
    """Test Startup removing by owner."""
    startup = startups[0]
    owner = startup.owner
    client.force_login(owner)
    url = reverse_lazy(
        "startups:startup_delete",
        kwargs={
            "pk": startup.pk
        },
    )
    response = client.post(url)
    assert response.status_code == 302
    assert models.Startup.objects.count() == len(startups) - 1


def test_startup_delete_view_not_owner(client, startups):
    """Test Startup removing by non-owner."""
    startup = startups[0]
    user = UserFactory()
    client.force_login(user)
    url = reverse_lazy(
        "startups:startup_delete",
        kwargs={
            "pk": startup.pk
        },
    )
    response = client.post(url)
    startup.refresh_from_db()
    assert response.status_code == 403
