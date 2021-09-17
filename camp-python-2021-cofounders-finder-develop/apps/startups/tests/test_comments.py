from django.urls import reverse_lazy

import pytest

from apps.comments.factories import CommentFactory
from apps.comments.models import Comment
from apps.startups import factories


@pytest.fixture(scope='module')
def startup():
    """Create new Startup instance."""
    created_startup = factories.StartupFactory()
    yield created_startup
    created_startup.delete()


@pytest.fixture
def url(startup):
    """Url for startup detail view."""
    return reverse_lazy(
        "startups:startup_detail",
        kwargs={"pk": startup.pk},
    )


@pytest.fixture
def parent_comment(startup):
    """Create new Comment instance without parent comment."""
    return CommentFactory(startup=startup)


def test_successful_save_comment_form(client, user, startup, url):
    """Test successful save form with valid data."""
    test_data = {
            "title": "Qwerty.",
            "text": "QwertyQwertyQwerty.",
            "parent_comment": "",
        }
    client.force_login(user)
    client.post(url, data=test_data)
    assert Comment.objects.filter(startup=startup, title="Qwerty.").exists()


def test_missing_title(client, user, startup, url):
    """Test raise validation error if missing title."""
    test_data = {
            "title": "",
            "text": "QwertyQwertyQwerty.",
            "parent_comment": "",
        }
    expected_errors = {"title": ["This field is required."], }
    client.force_login(user)
    response = client.post(url, data=test_data)
    assert response.context["form"].errors == expected_errors


def test_correct_parent_comment(client, user, url, parent_comment, startup):
    """Test add comment with correct parent comment."""
    test_data = {
            "title": "Some title",
            "text": "Some text",
            "parent_comment": parent_comment.id,
        }
    client.force_login(user)
    client.post(url, data=test_data)
    created_comment = startup.comments.get(parent_comment=parent_comment)
    assert created_comment.startup == parent_comment.startup


def test_get_startup_detail_and_comments(
        client,
        user,
        startup,
        url,
        parent_comment
):
    """Test get startup detail and comments."""
    response = client.get(url)
    response_startup = response.context["startup"]
    response_comment = response_startup.comments.first()
    assert response.status_code == 200
    assert response_startup.pk == startup.pk
    assert response_comment.title == parent_comment.title


def test_post_comment_anonymous_user(client, user, startup, url):
    """Test raise validation error if anonymous user try to post comment."""
    test_data = {
            "title": "Qwerty.",
            "text": "QwertyQwertyQwerty.",
            "parent_comment": "",
        }
    response = client.post(url, data=test_data)
    expected_errors = {'__all__': ['Sign in to post comments.']}
    assert response.context["form"].errors == expected_errors
