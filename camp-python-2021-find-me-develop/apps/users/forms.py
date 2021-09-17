from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.forms import ValidationError

from apps.users.constants import REVIEW_MARKS
from apps.users.models import BlackList, Review, User, UserReport


class SignUpForm(UserCreationForm):
    """Registration form for User."""

    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "bio",
                  "email", "password1", "password2",)

        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell about yourself"
                },
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email"
                },
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name"
                },
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name"
                },
            ),
        }

        labels = {"bio": "Bio"}

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            },
        ),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password confirmation"
            },
        ),
        label="Password confirm"
    )


class LogInForm(AuthenticationForm):
    """Log in form for user."""

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            },
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            },
        )
    )


class ResetPasswordForm(PasswordResetForm):
    """Password reset form for user."""

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email"
            },
        )
    )


class ResetPasswordConfirmForm(SetPasswordForm):
    """Set new password for user."""

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New password"
            },
        ),
        label="New password",
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New password confirm"
            },
        ),
        label="New password confirm",
    )


class UserEditForm(forms.ModelForm):
    """Form for change user info."""

    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "bio",
            "is_visible",
        )

        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "about me",
                },
            ),
        }

        labels = {
            "is_visible": "Is your location displayed on the map?"
        }


class UserReviewForm(forms.ModelForm):
    """For for review model."""

    class Meta:
        model = Review
        fields = ("title", "body", "rate",)

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                },
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Body (optional)",
                },
            ),
            "rate": forms.RadioSelect(
                choices=REVIEW_MARKS,
                attrs={
                    "class": "form-control",
                },
            ),
        }

    def clean(self):
        """Check that visitor not profile owner."""
        profile_owner_id = self.profile_owner_id
        request_user = self.request_user
        if not all([profile_owner_id is None, request_user is None]):
            if profile_owner_id == request_user.id:
                raise ValidationError("You cannot add review for yourself.")
            if request_user.reviews.filter(
                reviewed_id=profile_owner_id
            ).exists():
                raise ValidationError(
                    "You can't give a review to the same user twice."
                )
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        self.profile_owner_id = kwargs.pop("profile_owner_id", None)
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)


class UserReportForm(forms.ModelForm):
    """Create new report."""

    def __init__(self, created_by_id, reported_id, *args, **kwargs):
        """Set fields using parameters from view."""
        super().__init__(*args, **kwargs)
        self.instance.created_by_id = created_by_id
        self.instance.reported_id = reported_id

    class Meta:
        model = UserReport
        fields = ("reason",)

        widgets = {
            "reason": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "reason of report",
            }),
        }

    def save(self, commit=True):
        """Save the instance and check if the user is banned."""
        super().save(commit)
        self.instance.reported.ban_if_reached_limit()

    def clean(self):
        """Check if current user already report this user."""
        self.instance.validate_unique()
        super().clean()


class UserBlacklistForm(forms.ModelForm):
    """Create new blacklist item."""
    class Meta:
        model = BlackList
        fields = ("user", "banned_user")
