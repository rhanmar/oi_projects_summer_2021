from django.core.exceptions import ValidationError
from django.forms import ModelForm, inlineformset_factory

from apps.startups.models import Request

from . import models


class RequestForm(ModelForm):
    """Form to add new request to vacancy."""

    def __init__(self, user, vacancy, *args, **kwargs):
        """Set fields using parameters from view."""
        super().__init__(*args, **kwargs)
        self.user = user
        self.instance.vacancy = vacancy

    class Meta:
        model = Request
        fields = ("message", )

    def clean(self):
        """Check if user is anonymous."""
        if not self.user.is_anonymous:
            self.instance.user = self.user
        else:
            raise ValidationError(
                "Please sign up or log in for send request to this vacancy!"
            )
        super().clean()


class StartupForm(ModelForm):
    """Form for Startup."""
    class Meta:
        model = models.Startup
        fields = (
            "status",
            "title",
            "text",
            "end_date",
        )


class VacancyForm(ModelForm):
    """Form for Vacancy."""
    class Meta:
        model = models.Vacancy
        fields = (
            "status",
            "title",
            "description",
            "startup",
            "skills",
        )


VacancyFormSet = inlineformset_factory(
    models.Startup,
    models.Vacancy,
    form=VacancyForm,
    extra=1
)
