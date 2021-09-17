from django.contrib.contenttypes.models import ContentType
from django.core.validators import ValidationError

import pytest

from ..factories import TestContentTypeModel


@pytest.mark.parametrize("content_type,expected_output", [
    (
        {"app_label": "courses", "model": "course"},
        "courses.Course"
    ),
    (
        {"app_label": "users", "model": "user"},
        "users.User"
    ),
])
def test_get_model_name(
    content_type: dict, expected_output: str
):
    """Test `_get_model_name()` return str representation of model."""
    instance = TestContentTypeModel()
    content_type = ContentType.objects.get(
        app_label=content_type["app_label"],
        model=content_type["model"]
    )
    instance.content_type = content_type
    result = instance.get_model_name()
    assert result == expected_output


@pytest.mark.parametrize("content_type,allowed_models", [
    (
        {"app_label": "courses", "model": "course"},
        ["users.User", "courses.Topic"]
    ),
    (
        {"app_label": "courses", "model": "topic"},
        ["users.User", "courses.Course"]
    ),
    (
        {"app_label": "users", "model": "user"},
        ["courses.Task", "courses.Course", "courses.Topic"]
    ),
])
def test_clean_raises_exception(
    content_type: dict, allowed_models: str
):
    """Test `clean()` raises exception if `content_type`
    is not in `allowed_models`.
    """
    instance = TestContentTypeModel()
    instance.allowed_models = allowed_models
    content_type = ContentType.objects.get(
        app_label=content_type["app_label"],
        model=content_type["model"]
    )
    instance.content_type = content_type

    with pytest.raises(ValidationError):
        instance.clean()


@pytest.mark.parametrize("content_type,allowed_models", [
    (
        {"app_label": "users", "model": "user"},
        ("users.User", "courses.Topic")
    ),
    (
        {"app_label": "courses", "model": "course"},
        ("users.User", "courses.Course")
    ),
    (
        {"app_label": "courses", "model": "topic"},
        ("users.User", "courses.Course", "courses.Topic")
    ),
])
def test_clean(content_type: dict, allowed_models: tuple):
    """Test `clean()` not raises exception if `content_type`
    is in `allowed_models`.
    """
    instance = TestContentTypeModel()
    instance.allowed_models = allowed_models
    content_type = ContentType.objects.get(
        app_label=content_type["app_label"],
        model=content_type["model"]
    )
    instance.content_type = content_type
    try:
        instance.clean()
    except ValidationError as exc:
        assert False, f"Raised an exception {exc}"
