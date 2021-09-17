from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from apps.comments.forms import CommentForm
from apps.core.mixins import PostFormMixin
from apps.startups import forms, models


class CheckStartupOwnerMixin(UserPassesTestMixin):
    """Mixin to check whether the user is the owner of the startup."""

    def test_func(self):
        """Check whether the user is owner of startup."""
        return self.get_object().owner == self.request.user


class StartupBaseView:
    """Base view for Startup."""

    model = models.Startup
    form_class = forms.StartupForm
    success_url = reverse_lazy("startups:startups_list")
    login_url = reverse_lazy("login")


class StartupsListView(generic.ListView):
    """Show all startups."""

    queryset = models.Startup.objects.select_related(
        "owner"
    ).active().order_by("-created")
    context_object_name = "startups"
    template_name = "startups/startup_list.html"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data()
        data["startups_amount"] = models.Startup.objects.cache(
            ops=["count"]
        ).count()
        return data


class StartupsDetailView(PostFormMixin, generic.DetailView):
    """Show info about given startup and add comments to startup."""
    template_name = "startups/startup_detail.html"
    context_object_name = "startup"
    form_class = CommentForm
    queryset = models.Startup.objects.all().select_related(
        "owner"
    ).prefetch_related(
        "comments__author",
        "vacancies",
    )

    def get_form_kwargs(self):
        """Send request params to form init as kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "author": self.request.user,
            "startup": self.get_object(),
        })
        return kwargs

    def get_success_url(self):
        """URL to redirect in case of successful comment creation."""
        return self.request.path


class StartupCreateEditMixin:
    """Mixin to remove duplicity in StartupCreateView and StartupUpdateView."""

    def __init__(self, *args, **kwargs):
        """Initialize the object."""
        super().__init__(*args, **kwargs)
        self.object = None

    def form_invalid(self, vacancies_formset):
        """Resend the form."""
        context = self.get_context_data()
        context["vacancies_formset"] = vacancies_formset
        return self.render_to_response(context)

    def form_valid(self, startup_form, vacancies_formset):
        """Save data from form."""
        startup_form.save()
        vacancies_formset.save()
        return HttpResponseRedirect(reverse_lazy("startups:startups_list"))

    def get_context_data(self, **kwargs):
        """Add  extra data to context."""
        context = super().get_context_data(**kwargs)
        if "vacancies_formset" not in context:
            if self.create is True:
                context["vacancies_formset"] = forms.VacancyFormSet()
            else:
                context["vacancies_formset"] = forms.VacancyFormSet(
                    instance=self.get_object()
                )
        return context

    def post(self, request, *args, **kwargs):
        """Create or Update Startup from POST request."""
        startup_form = kwargs["startup_form"]
        vacancies_formset = forms.VacancyFormSet(
            request.POST,
            instance=startup_form.instance
        )
        if not all([startup_form.is_valid(), vacancies_formset.is_valid()]):
            return self.form_invalid(vacancies_formset)
        return self.form_valid(startup_form, vacancies_formset)


class StartupCreateView(
    StartupCreateEditMixin,
    StartupBaseView,
    LoginRequiredMixin,
    generic.CreateView,
):
    """Create a new Startup."""

    template_name = "startups/startup_create.html"
    create = True

    def post(self, request, *args, **kwargs):
        """Create a new Startup from POST request."""
        startup_form = self.get_form()
        if not startup_form.is_valid():
            return self.form_invalid(
                forms.VacancyFormSet(request.POST)
            )
        current_startup = startup_form.save(commit=False)
        current_startup.owner = self.request.user
        kwargs["startup_form"] = startup_form
        return super().post(request, *args, **kwargs)


class StartupUpdateView(
    StartupCreateEditMixin,
    StartupBaseView,
    CheckStartupOwnerMixin,
    LoginRequiredMixin,
    generic.UpdateView
):
    """Update the Startup."""

    template_name = "startups/startup_update.html"
    create = False

    def post(self, request, *args, **kwargs):
        """Update the Startup instance from POST request."""
        self.object = self.get_object()
        kwargs["startup_form"] = self.get_form()
        return super().post(request, *args, **kwargs)


class StartupDeleteView(
    StartupBaseView,
    CheckStartupOwnerMixin,
    LoginRequiredMixin,
    generic.DeleteView
):
    """Delete the Startup."""

    template_name = "startups/startup_delete.html"
