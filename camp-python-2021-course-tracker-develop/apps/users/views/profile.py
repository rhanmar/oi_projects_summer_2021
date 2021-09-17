from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from apps.users.forms import UserLinkFormset, UserUpdateForm
from apps.users.models import User


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Implement user's profile change logic."""

    model = User
    form_class = UserUpdateForm
    formset_class = UserLinkFormset
    template_name = "users/profile/update_profile.html"
    success_url = reverse_lazy("homepage")
    object = None

    def get_object(self, queryset=None):
        """Return current user as an object."""
        return self.request.user

    def post(self, request, *args, **kwargs):
        """Save formset information instance."""
        self.object = self.get_object()
        form = self.get_form()
        formset = self.formset_class(
            self.request.POST, instance=self.get_object()
        )
        if not all((formset.is_valid(), form.is_valid(),)):
            return self.form_invalid(form, formset=formset)
        formset.save()
        return self.form_valid(form)

    def form_invalid(self, form, **kwargs):
        """Add to page which open after error current context."""
        context = self.get_context_data()
        context["formset"] = kwargs["formset"]
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Append user links formset to context."""

        formset = self.formset_class(instance=self.object)

        kwargs["formset"] = formset
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        """Return url after success update profile."""
        return reverse_lazy("user", kwargs={"pk": self.request.user.id})
