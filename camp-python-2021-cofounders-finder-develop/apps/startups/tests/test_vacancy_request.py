from django.urls import reverse

import pytest

from apps.startups import factories
from apps.startups.models import Request


@pytest.fixture(scope='module')
def vacancy():
    """Create new Vacancy instance."""
    created_vacancy = factories.VacancyFactory()
    yield created_vacancy
    created_vacancy.delete()


@pytest.fixture
def url(vacancy):
    """Url for vacancy detail view."""
    return reverse(
        "startups:vacancy_detail",
        kwargs={
            "pk": vacancy.pk
        }
    )


@pytest.fixture
def request_to_vacancy(vacancy, user):
    """Create new Request instance."""
    return factories.RequestFactory(vacancy=vacancy, user=user)


def test_successful_send_request_to_vacancy(client, user, url, vacancy):
    """Test successful sending request to vacancy."""
    test_data = {"message": "qwerty"}
    client.force_login(user)
    response = client.post(url, data=test_data)
    created_request = Request.objects.filter(
        vacancy=vacancy,
        message="qwerty",
        user=user,
    )
    assert response.status_code == 302
    assert created_request.exists()


def test_request_to_vacancy_already_sent(client, user, url, vacancy):
    """Test raise validation error if user already sent request to vacancy."""
    test_data = {"message": "123"}
    client.force_login(user)
    client.post(url, data=test_data)
    response = client.post(url, data=test_data)
    expected_errors = {
        '__all__': ['Request with this User and Vacancy already exists.']
    }
    assert response.context["form"].errors == expected_errors


def test_anonymous_user_request_to_vacancy(client, user, url, vacancy):
    """Test raise validation error if anonymous user try to sent request."""
    test_data = {"message": "123"}
    response = client.post(url, data=test_data)
    expected_errors = {
        '__all__': [
            'Please sign up or log in for send request to this vacancy!'
        ]
    }
    assert response.context["form"].errors == expected_errors


def test_successful_get_vacancy_and_requests(
        client,
        user,
        url,
        vacancy,
        request_to_vacancy,
):
    """Test get vacancy detail and requests."""
    response = client.get(url)
    response_vacancy = response.context["vacancy"]
    response_request = response_vacancy.requests.first()
    assert response_vacancy == vacancy
    assert response_request == request_to_vacancy
