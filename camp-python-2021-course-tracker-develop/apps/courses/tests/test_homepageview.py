from django.urls import reverse

import pytest

from .factories import CourseFactory

homepage_url = reverse("homepage")


@pytest.fixture
def course(auth_user):
    """Fixture for returning Course instance."""
    course_instance = CourseFactory.create()
    course_instance.users.add(auth_user)
    return course_instance


def test_return_course(auth_user, client, course):
    """Test view returns users last course."""
    response = client.get(homepage_url, follow=True)

    assert response.status_code == 200

    resp_course = response.context_data["course"]

    assert resp_course.pk == course.pk
    assert resp_course.title == course.title
    assert resp_course.description == course.description
