from django.urls import reverse

import pytest

from .factories import TaskFactory


@pytest.fixture
def task():
    """Fixture of Task."""
    return TaskFactory.create()


def test_task_view_page(client, task, auth_user):
    """Test `TaskDetailView` return correct data."""
    response = client.get(
        reverse("task-detail", args=[task.id]),
        follow=True,
    )
    assert response.status_code == 200
    assert response.context_data["task"] == task
