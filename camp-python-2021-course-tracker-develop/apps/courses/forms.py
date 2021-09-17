from django import forms

from . import models
from .constants import TOPIC_DAY_DELTA_CHOICES
from .models import Course


class AddCommentForm(forms.ModelForm):
    """Form for add new comment."""

    parent = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )

    class Meta:
        model = models.Comment
        fields = ("text",)

    def __init__(self, content_type, **kwargs):
        """Constructor that add content type of comment to the instance.

        Args:
            content_type(ContentType): for what model comment will be added.

        """
        super().__init__(**kwargs)
        self.instance.content_type = content_type


class SolutionForm(forms.ModelForm):
    """Form for solution."""

    class Meta:
        model = models.Solution
        fields = (
            "solution_description",
            "attachment",
        )


class EvaluationForm(forms.ModelForm):
    """Form for evaluation"""

    class Meta:
        model = models.Evaluation
        fields = (
            "mark",
            "comment",
        )


class ScheduleInfoForm(forms.Form):
    """Form for add schedule info for course and planning system."""

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    course = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}),
        queryset=Course.objects.all(),
    )

    def __init__(self, **kwargs):
        """Constructor."""
        super().__init__(**kwargs)
        course = kwargs["initial"]["course"]
        default_speaker = kwargs["initial"]["default_speaker"]
        self.fields["default_speaker"] = forms.ModelChoiceField(
            widget=forms.Select(attrs={"class": "form-select"}),
            queryset=course.users.mentors(),
            initial=default_speaker,
        )


class TopicBecomeSpeakerForm(forms.Form):
    """Form for set current user as speaker."""

    topic_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={"id": "topic_id_for_speaker"})
    )


class RescheduleTopicForm(forms.Form):
    """Form for change reading date for topic."""

    topic_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={"id": "topic_id_for_reschedule"})
    )
    day_delta = forms.TypedChoiceField(
        choices=TOPIC_DAY_DELTA_CHOICES,
        coerce=int,
    )
