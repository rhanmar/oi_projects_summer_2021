from django.core.exceptions import ValidationError

import pytest

from ..models.users import User


def test_unique_email_validation(user):
    """Test validation for case insensitive unique email."""
    new_user = User(email=user.email.upper(), password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
    assert "email" in exc.value.error_dict
