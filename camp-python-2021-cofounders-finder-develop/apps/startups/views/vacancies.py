from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import generic

from apps.core.mixins import PostFormMixin
from apps.startups import forms, models
from apps.startups.forms import RequestForm


class CheckVacancyOwnerMixin(UserPassesTestMixin):
    """Mixin to check whether the user is a startup owner in the vacancy."""

    def test_func(self):
        """Check whether the user is a startup owner in the vacancy."""
        return self.get_object().startup.owner == self.request.user


class VacancyBaseView:
    """Base view for Vacancy."""

    model = models.Vacancy
    form_class = forms.VacancyForm
    success_url = reverse_lazy("startups:vacancies_list")
    login_url = reverse_lazy("login")


class VacanciesListView(generic.ListView):
    """Show all vacancies."""

    queryset = models.Vacancy.objects.select_related("startup")
    context_object_name = "vacancies"
    template_name = "startups/vacancy_list.html"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        """Add `vacancies_amount` to context."""
        data = super().get_context_data()
        data["vacancies_amount"] = models.Vacancy.objects.cache(
            ops=["count"]
        ).count()
        return data


class VacancyDetailView(PostFormMixin, generic.DetailView):
    """Show info about given vacancy and send request to vacancy."""
    context_object_name = "vacancy"
    template_name = "startups/vacancy_detail.html"
    form_class = RequestForm
    queryset = models.Vacancy.objects.select_related(
        "startup"
    ).prefetch_related(
        "skills",
        "employees__user",
        "requests__user",
    )

    def get_form_kwargs(self):
        """Send request params to form init as kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs.update({
            "user": self.request.user,
            "vacancy": self.get_object(),
        })
        return kwargs

    def get_success_url(self):
        """URL to redirect in case of successful request creation."""
        return self.request.path


class VacancyUpdateView(
    VacancyBaseView,
    CheckVacancyOwnerMixin,
    LoginRequiredMixin,
    generic.UpdateView
):
    """Update the Vacancy."""

    template_name = "startups/vacancy_update.html"


class VacancyDeleteView(
    CheckVacancyOwnerMixin,
    LoginRequiredMixin,
    VacancyBaseView,
    generic.DeleteView
):
    """Delete the Vacancy."""

    template_name = "startups/vacancy_delete.html"
