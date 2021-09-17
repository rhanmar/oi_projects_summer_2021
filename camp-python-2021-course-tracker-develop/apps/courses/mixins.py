from django.contrib.auth.mixins import AccessMixin


class MentorRequiredMixin(AccessMixin):
    """Mixing that checks user is mentor."""

    def dispatch(self, request, *args, **kwargs):
        """Get access to view if user is mentor."""
        if not request.user.is_mentor():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
