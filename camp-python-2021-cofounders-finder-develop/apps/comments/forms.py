from django import forms
from django.core.exceptions import ValidationError

from apps.comments.models import Comment


class CommentForm(forms.ModelForm):
    """Form to add new comment."""

    def __init__(self, author, startup, *args, **kwargs):
        """Set fields using parameters from view."""
        super().__init__(*args, **kwargs)
        self.author = author
        self.instance.startup = startup

    class Meta:
        model = Comment
        fields = ("title", "text", "parent_comment",)

    def clean(self):
        """Raise validation error if anonymous user try to post comment."""
        if not self.author.is_anonymous:
            self.instance.author = self.author
        else:
            raise ValidationError("Sign in to post comments.")
        super().clean()
