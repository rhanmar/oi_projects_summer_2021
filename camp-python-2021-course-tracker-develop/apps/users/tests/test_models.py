from django.core.exceptions import ValidationError

import pytest

from ..models import User
from ..validators import validate_email_domain


def test_unique_email_validation(user):
    """Test validation for case insensitive unique email."""
    new_user = User(email=user.email.upper(), password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
    assert "email" in exc.value.error_dict


def test_allowed_email_domains_validation(user):
    """Ensure that email domain is allowed and user can be added to db."""
    new_user = User(email=user.email, password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
        validate_email_domain(new_user.email)
    assert "email" in exc.value.error_dict
