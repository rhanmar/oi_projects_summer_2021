from django.urls import reverse_lazy

import pytest

from apps.courses.tests.factories import (
    SolutionFactory,
    create_filled_in_factory,
)


@pytest.fixture()
def course():
    """Fixture for returning Course instance."""
    return create_filled_in_factory()


@pytest.fixture()
def solution(course):
    """Fixture for returning solution with user in course."""
    user = course.users.filter(is_staff=False).last()
    task = course.chapters.last().topics.last().tasks.last()
    return SolutionFactory.create(owner=user, task=task)


@pytest.fixture()
def solution_user(solution, client):
    """Fixture for returning user which solution owner and logging in."""
    user = solution.owner
    client.force_login(user)
    return user


@pytest.fixture()
def course_user(course, client):
    """Fixture for returning user which course member and logging in."""
    user = course.users.filter(is_staff=False).first()
    client.force_login(user)
    return user


@pytest.mark.parametrize("test_data", [
    {"solution_description": "Hello world!"},
    {"solution_description": "Hello world1!"},
    {"solution_description": 234},
])
def test_create_solution(course, client, course_user, test_data):
    """Test create solution for tusk by current user."""

    task = course.chapters.first().topics.first().tasks.first()
    response = client.post(
        reverse_lazy("task-detail", kwargs={"pk": task.pk}),
        data=test_data,
    )
    course_user.refresh_from_db()
    assert response.status_code == 302
    for key, value in test_data.items():
        assert getattr(course_user.solutions.first(), key) == str(value)


@pytest.mark.parametrize("test_data", [
    {"solution_description": "Hello world!"},
    {"solution_description": "Hello world1!"},
    {"solution_description": 234},
])
def test_update_solution(solution, client, solution_user, test_data):
    """Test update solution for tusk by current user."""

    task = solution.task
    response = client.post(
        reverse_lazy("task-detail", kwargs={"pk": task.pk}),
        data=test_data,
    )
    solution_user.refresh_from_db()
    assert response.status_code == 302
    for key, value in test_data.items():
        assert getattr(solution_user.solutions.first(), key) == str(value)


def test_validation(course, solution, course_user, client):
    """Test validation of create solution for tusk by current user."""
    task = course.chapters.first().topics.first().tasks.first()
    test_data = {
        "solution_description": "",
    }
    expected_errors = {
        "solution_description": ["This field is required."],
    }
    response = client.post(
        reverse_lazy("task-detail", kwargs={"pk": task.pk}),
        data=test_data,
    )
    assert response.context["form"].errors == expected_errors
