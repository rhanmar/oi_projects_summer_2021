from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from libs.notifications.email import DefaultEmailNotification

from .models import User, UserLink

__all__ = (
    "CustomUserCreationForm",
    "UserUpdateForm",
    "UserLinkFormset",
    "CustomPasswordResetForm",
)


class CustomUserCreationForm(UserCreationForm):
    """Custom form to register new user."""

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2"
        )


class UserUpdateForm(UserChangeForm):
    """Form to update user instance.

    Setting password to None to override parent class redundant behaviour.
    """

    password = None

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "github_username",
        )
        widgets = {
            "profile_image": forms.FileInput(),
            "bio": forms.Textarea(attrs={"placeholder": "Your bio"}),
        }


# Formset to display all user links
UserLinkFormset = inlineformset_factory(
    User,
    UserLink,
    fields=("title", "url"),
    extra=1,
)


class CustomPasswordResetForm(forms.Form):
    """Custom form to reset user's password."""

    email = forms.EmailField(
        help_text="Email of account which password should be reset"
    )

    _token_generator = default_token_generator

    def __init__(self, *args, **kwargs):
        """Override super __init__ to add _user field.

        Adds _user field that is initially None and sets it to user instance
        while calling ``validate_email``.
        """
        super().__init__(*args, **kwargs)
        self._user = None

    def send_mail(self):
        """Send email with link for password reset to specified user."""
        return DefaultEmailNotification(
            subject=_("Password reset"),
            recipient_list=[self._user.email],
            template="users/emails/password_reset.html",
            uid=urlsafe_base64_encode(force_bytes(self._user.pk)),
            token=self._token_generator.make_token(self._user),
            app_url=settings.FRONTEND_URL,
            app_label=settings.APP_LABEL,
        ).send()

    def validate_email(self, email: str):
        """Check if user with specified email exists."""
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError(
                _("There is no user with such email")
            )
        self._user = query.first()

    def save(self):
        """Send email if user with provided email exists."""
        self.validate_email(self.cleaned_data["email"])
        self.send_mail()
