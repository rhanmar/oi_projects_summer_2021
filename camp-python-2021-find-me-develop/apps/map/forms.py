from django import forms

from apps.map.models import Meeting, MeetingReview
from apps.users.constants import REVIEW_MARKS


class MeetingForm(forms.ModelForm):
    """Form for Meeting model."""
    class Meta:
        model = Meeting
        fields = (
            "title",
            "description",
            "max_people_limit",
            "photo",
            "deadline",
        )

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of meeting",
            }),
            "max_people_limit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 100,
                }
            ),
        }

        labels = {
            "title": "Title",
            "description": "Description",
            "max_people_limit": "How much people can join to you?",
            "photo": "Photo (optional)",
            "deadline": "Deadline",
        }

    def save(self, commit=True):
        instance = super().save(commit)
        location = instance.location
        location.title = instance.title
        location.save()
        return instance


class MeetingReviewForm(forms.ModelForm):
    """Form to make a review on meeting."""

    class Meta:
        model = MeetingReview
        fields = (
            "title",
            "body",
            "rate",
        )
        labels = {
            "body": "Text",
        }
        widgets = {
            "rate": forms.RadioSelect(
                choices=REVIEW_MARKS,
                attrs={"class": "form-control"},
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Title",
                },
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Text of your review",
                },
            ),
        }
