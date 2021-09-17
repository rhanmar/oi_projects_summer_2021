from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from apps.users.models import CV, EvaluationInfo, Url, User


class EmailUserForm(UserCreationForm):
    """Custom form to register new user."""

    class Meta:
        model = User
        fields = ("email", "password1", "password2",)


UrlsFormSet = inlineformset_factory(
    parent_model=User,
    model=Url,
    fields=("name", "url",),
    extra=1,
)


class SkillEvaluationForm(forms.ModelForm):
    """Custom form to add review about certain skill of certain user cv."""

    def __init__(self, owner, *args, **kwargs):
        """Set fields using parameters from view."""
        super().__init__(*args, **kwargs)
        self.owner = owner

    BOOLEAN_CHOICES = (("True", "Approve"), ("False", "Opposite"))
    is_approved = forms.ChoiceField(
        label=_("Is approved?"),
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
        initial="True",
    )

    def clean(self):
        """Raise validation error if anonymous user try to evaluate skill."""
        if not self.owner.is_anonymous:
            self.instance.owner = self.owner
        else:
            raise ValidationError("Sign in to evaluate skills.")

    class Meta:
        model = EvaluationInfo
        fields = ("comment", "is_approved", "skill_from_cv",)
        widgets = {
            "skill_from_cv": forms.HiddenInput(),
        }


class CVForm(forms.ModelForm):
    """Form for creation new CV."""

    def __init__(self, owner, *args, **kwargs):
        """Set fields using parameters from view."""
        super().__init__(*args, **kwargs)
        self.owner = owner

    class Meta:
        model = CV
        fields = ("title", "description", "skills",)

    def clean(self):
        """Raise validation error if anonymous user try to evaluate skill."""
        if not self.owner.is_anonymous:
            self.instance.owner = self.owner
        else:
            raise ValidationError("Sign in to create CV.")
