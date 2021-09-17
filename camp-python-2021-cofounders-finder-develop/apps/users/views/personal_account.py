from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView

from .. import models
from ..forms import CVForm, UrlsFormSet


class CurrentUserMixin(LoginRequiredMixin):
    """Mixin for add to view-model information about the current user."""

    model = models.User

    def get_object(self):
        """Return current user instance to view instance."""
        return self.request.user


class UserDetailView(
    CurrentUserMixin,
    generic.DetailView,
):
    """View for render information about current user."""

    template_name = "users/accounts/account.html"


class UserUpdateView(
    CurrentUserMixin,
    generic.UpdateView,
):
    """View for update information about current user."""

    template_name = "users/accounts/account_update.html"
    fields = ("first_name", "last_name", "email", "location", "avatar")

    def __init__(self, **kwargs):
        """Initialize self object."""
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        """Add formset context to context of view."""
        context = super().get_context_data(
            **kwargs
        )
        context["formset"] = UrlsFormSet(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        """Save formset information instance."""
        self.object = self.get_object()
        form = self.get_form()
        formset = UrlsFormSet(
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

    success_url = reverse_lazy("account")


class CurrentUserCVsMixin(LoginRequiredMixin):
    """Mixin for add to view-model information about cvs of current user."""

    model = models.CV

    def get_queryset(self):
        """Return cvs of current user instance to view instance."""
        return self.request.user.cvs.all()


class CurrentUserCVsView(CurrentUserCVsMixin, ListView):
    """View for render list of current user's cvs."""
    context_object_name = "cvs"
    template_name = "users/cvs/cvs_list.html"


class CurrentUserCVDetailView(
        CurrentUserCVsMixin,
        generic.DetailView,
):
    """View for render information about cv of current user."""
    context_object_name = "cv"
    template_name = "users/cvs/current_cv.html"


class CurrentUserCVUpdateView(
        CurrentUserCVsMixin,
        generic.UpdateView,
):
    """View for update information about cv of current user."""

    template_name = "users/cvs/cv_update.html"
    fields = ("title", "description", "skills",)
    success_url = reverse_lazy("account_cvs")


class CurrentUserCVCreateView(LoginRequiredMixin, generic.CreateView,):
    """View for creation cv of current user."""

    template_name = "users/cvs/cv_create.html"
    form_class = CVForm
    success_url = reverse_lazy("account_cvs")

    def get_form_kwargs(self):
        """Send user request params to form init as kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({"owner": self.request.user})
        return kwargs


class CurrentUserCVDeleteView(
        CurrentUserCVsMixin,
        generic.DeleteView,
):
    """View for delete information about cv of current user."""

    success_url = reverse_lazy("account")
