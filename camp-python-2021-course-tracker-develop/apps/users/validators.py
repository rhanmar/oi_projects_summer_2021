from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

__all__ = (
    "validate_email_domain",
)

from django.conf import settings


def validate_email_domain(email: str):
    """Check if email has right domain.

    Args:
        email: user's email.

    Raises:
        ValidationError: if email domain not allowed.
    """
    domain_part = email.strip().rsplit("@", 1)[-1]

    if domain_part not in settings.ALLOWED_USER_EMAIL_DOMAINS:
        raise ValidationError(
            _(f"You cannot register with {domain_part} domain."),
            code="wrong_email_domain"
        )
