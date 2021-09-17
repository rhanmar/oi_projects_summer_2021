from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views import generic

from apps.core.mixins import PostFormMixin
from apps.users import models
from apps.users.forms import SkillEvaluationForm
from apps.users.models import CVSkillEvaluation


class CVsListView(generic.ListView):
    """Show all startups."""
    queryset = models.CV.objects.select_related("owner")
    context_object_name = "cvs"
    template_name = "cvs/cv_list.html"
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        """Add `cvs_amount` to docstring."""
        data = super().get_context_data(**kwargs)
        data["cvs_amount"] = models.CV.objects.cache(ops=["count"]).count()
        return data


class CVsDetailView(PostFormMixin, LoginRequiredMixin, generic.DetailView):
    """Show info about cv and give opportunity to add review of cv skills."""

    template_name = "cvs/cv_detail.html"
    context_object_name = "cv"
    queryset = models.CV.objects.select_related(
        "owner",
    ).prefetch_related(
        Prefetch(
            "evaluate_skills",
            queryset=CVSkillEvaluation.objects.with_count_of_evaluations()
        ),
        "evaluate_skills__evaluated_skill__owner",
        "evaluate_skills__evaluations",
        "evaluate_skills__skill",
    )
    form_class = SkillEvaluationForm

    def get_context_data(self, **kwargs):
        """Add to context forms for everyone skills of certain cv."""
        context = super().get_context_data(**kwargs)
        current_cv = self.object
        form = kwargs.get("form")
        if current_cv.owner.id != self.request.user.id:
            forms = []
            for skill in current_cv.evaluate_skills.all():
                if form and form.instance.skill_from_cv_id == skill.id:
                    forms.append(form)
                else:
                    new_form = self.form_class(self.get_form_kwargs())
                    new_form.fields["skill_from_cv"].initial = skill
                    forms.append(new_form)
            context["forms"] = forms
        return context

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        """Send user request params to form init as kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["owner"] = self.request.user
        return kwargs
