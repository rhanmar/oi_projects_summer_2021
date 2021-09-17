from django.urls import reverse

import pytest

from apps.core.factories import SkillFactory
from apps.startups import factories, models
from apps.users.factories import UserFactory


@pytest.fixture
def vacancy_with_2_skills():
    skills = SkillFactory.create_batch(2)
    return factories.VacancyFactory.create(skills=skills)


def test_vacancies_list_view(client, vacancies):
    """Test that vacancies_list returns list of vacancies."""
    url = reverse("startups:vacancies_list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["vacancies"].count() == len(vacancies)


def test_vacancy_detail_view_title(client, vacancies):
    """Test that vacancy_detail returns valid Vacancy title."""
    url = reverse(
        "startups:vacancy_detail",
        kwargs={
            "pk": vacancies[0].pk
        }
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["vacancy"].title == vacancies[0].title


def test_vacancy_update_view_unauthorized(client, vacancies):
    vacancy = vacancies[0]
    url = reverse(
        "startups:vacancy_update",
        kwargs={
            "pk": vacancy.pk
        }
    )
    response = client.get(url)
    assert response.url.split("?next")[0] == reverse("login")


@pytest.mark.parametrize(
    "test_data,errors", [
        (
            {
                "status": "open",
                "title": "vac1",
                "description": "description1",
                "skills": "",
                "startup": "",
            },
            {
                'skills': ['“” is not a valid value.'],
                'startup': ['This field is required.']
            }
        ),
    ],
)
def test_vacancy_update_view_invalid(client, vacancies, test_data, errors):
    """Test Vacancy update by owner with invalid data."""
    vacancy = vacancies[0]
    owner = vacancy.startup.owner
    client.force_login(owner)
    url = reverse(
        "startups:vacancy_update",
        kwargs={
            "pk": vacancy.pk
        }
    )
    response = client.post(url, data=test_data)
    assert response.status_code == 200
    assert response.context["form"].errors == errors


def test_vacancy_update_view_non_owner(client, vacancies):
    """Test Vacancy update by non-owner."""
    user = UserFactory()
    vacancy = vacancies[0]
    client.force_login(user)
    url = reverse(
        "startups:vacancy_update",
        kwargs={
            "pk": vacancy.pk
        },
    )
    response = client.post(url)
    assert response.status_code == 403


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "status": "open",
            "title": "vac1",
            "description": "description1",
            "skills": [1, 2, 3],
        }
    ],
)
def test_vacancy_update_view_valid(client, vacancy_with_2_skills, test_data):
    """Test Vacancy update by owner with valid data."""
    owner = vacancy_with_2_skills.startup.owner
    test_data["startup"] = vacancy_with_2_skills.startup.pk
    client.force_login(owner)
    url = reverse(
        "startups:vacancy_update",
        kwargs={
            "pk": vacancy_with_2_skills.pk
        }
    )
    response = client.post(url, data=test_data)
    updated_vacancy = models.Vacancy.objects.get(pk=vacancy_with_2_skills.pk)
    assert response.status_code == 302
    assert updated_vacancy.title == test_data["title"]
    assert updated_vacancy.description == test_data["description"]
