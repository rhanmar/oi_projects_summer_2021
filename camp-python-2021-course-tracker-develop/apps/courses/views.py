from datetime import timedelta

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import (
    DeleteView,
    FormMixin,
    FormView,
    UpdateView,
)

from . import forms, models
from .mixins import MentorRequiredMixin


class HomePageView(TemplateView):
    """Represent main page with course info and lectures plan.

    Return context with last added course.
    """

    template_name = "index/index.html"

    def get_context_data(self, **kwargs):
        """Return custom context with course."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = user.courses.prefetch_related(
            "chapters__topics__speaker",
        )
        current_queryset = queryset.last()
        course = queryset.not_hidden().last()
        if course:
            is_visitor_mentor = course.users.get(id=user.id).is_mentor()
            context["course"] = current_queryset
            course_with_marks = user.courses.all_with_solution_mark(
                user
            ).last()

            context["course_rating"] = 0.0
            if course_with_marks:
                context["course_rating"] = course_with_marks.course_progress()

            context["now"] = timezone.now().date()
            context["is_visitor_mentor"] = is_visitor_mentor
            context["form_become_speaker"] = forms.TopicBecomeSpeakerForm()
            context["form_reschedule_topic"] = forms.RescheduleTopicForm()

        return context


class TopicView(DetailView):
    """View for chosen Topic with tasks."""
    template_name = "courses/topic.html"
    model = models.Topic

    def get_queryset(self):
        """Return queryset of topics with prefetched data."""
        return models.Topic.objects.all().prefetch_related(
            Prefetch(
                "comments",
                queryset=models.Comment.objects
                .parent_comments_in_reverse_order()
                .prefetch_related(
                    Prefetch(
                        "sub_comments",
                        queryset=models.Comment.objects
                        .child_comments_in_order(),
                        to_attr="child_comments",
                    )
                ),
                to_attr="parent_comments",
            )
        )

    def get_context_data(self, **kwargs):
        """Return custom context with not hidden tasks."""
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["object"].tasks.all()
        topics_with_rating = models.Topic.objects.all_with_solution_mark(
            self.request.user
        )
        context["topic_rating"] = 0.0
        if topics_with_rating.filter(id=self.kwargs["pk"]):
            context["topic_rating"] = topics_with_rating.get(
                id=self.kwargs["pk"]
            ).topic_rating()

        return context


class TaskDetailView(DetailView, FormMixin):
    """Represent DetailView of Task model."""

    model = models.Task
    template_name = "courses/task.html"
    form_class = forms.SolutionForm

    def __init__(self, **kwargs):
        """Initialize current object."""
        super().__init__(**kwargs)
        self.object = None

    def get_queryset(self):
        """Return queryset of Tasks."""
        return models.Task.objects.not_hidden().prefetch_related(
            Prefetch(
                "comments",
                queryset=models.Comment.objects
                .parent_comments_in_reverse_order()
                .prefetch_related(
                    Prefetch(
                        "sub_comments",
                        queryset=models.Comment.objects
                        .child_comments_in_order(),
                        to_attr="child_comments",
                    )
                ),
                to_attr="parent_comments",
            )
        )

    def get_context_data(self, **kwargs):
        """Add to context instance of form if not solution of current user."""
        context = super().get_context_data(**kwargs)
        task = self.object

        if not task.solutions.filter(
            owner=self.request.user
        ).exists() or context["form"].errors:
            return context

        return self.add_form_to_context(context)

    def add_form_to_context(self, context):
        """Add solution form to context and initialize description field.

        Args:
            context: current context.
        """
        solution_form = self.get_form()
        current_user_id = self.request.user.pk
        solution_form.fields["solution_description"].initial = (
            self.object.solutions.filter(
                owner_id=current_user_id
            ).get().solution_description
        )
        current_solution = self.object.solutions.get(
            owner_id=current_user_id
        )
        context["current_solution"] = current_solution
        context["form"] = solution_form
        return context

    def post(self, request, *args, **kwargs):
        """Call form valid function and init form instance."""
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """Bound solution with current user and current task.

        If solution not created yet create new solution instance, else
        update solution description field.
        """

        solution_form_instance = form.save(commit=False)
        self.add_to_solution_missing_fields_value(solution_form_instance)

        return HttpResponseRedirect(self.request.path)

    def add_to_solution_missing_fields_value(self, solution_form_instance):
        """Add to solution value of missing fields.

        If method - create:
            add to owner field current user
            add to task field current task
        If method - update:
            update solution_description field

        Args:
            solution_form_instance: instance of solution which user fill up
            before post.
        """

        solution = self.object.solutions.filter(
            owner=self.request.user
        ).first()

        files = self.request.FILES

        if not solution:
            solution_form_instance.owner = self.request.user
            solution_form_instance.task = self.object
            if files:
                solution_form_instance.attachment = files["attachment"]
            solution_form_instance.save()

        else:
            solution.solution_description = (
                solution_form_instance.solution_description
            )
            if files:
                solution.attachment = files["attachment"]
            solution.save()


class MyTasksView(TemplateView):
    """Represent MyTasks page with pre rendered chapters buttons."""

    template_name = "courses/mytasks.html"

    def get_context_data(self, **kwargs):
        """Return related to users course chapters."""
        context = super().get_context_data(**kwargs)

        course = self.request.user.courses.not_hidden().last()
        if course:
            context["chapters"] = course.chapters.not_hidden()
        return context


class AutoPlanningView(MentorRequiredMixin, FormView):
    """View for planning course schedule."""

    template_name = "courses/planning_form.html"
    form_class = forms.ScheduleInfoForm
    success_url = reverse_lazy("homepage")
    course = None

    def get(self, request, *args, **kwargs):
        """Http method GET."""
        self.course = models.Course.objects.get(id=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Http method POST."""
        self.course = models.Course.objects.get(id=self.kwargs["pk"])
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        """Return initial dict for form."""
        return {
            "course": self.course,
            "default_speaker": self.request.user,
        }

    def get_context_data(self, **kwargs):
        """Return custom context with course object."""
        context = super().get_context_data(**kwargs)
        context["course"] = self.course
        return context

    def form_valid(self, form):
        """Plan schedule for chosen course."""
        cleaned_data = form.cleaned_data
        course = cleaned_data["course"]
        current_date = cleaned_data["start_date"]

        for chapter in course.chapters.all():
            chapter.start_date = current_date

            for topic in chapter.topics.all():
                topic.reading_date = current_date
                topic.speaker = None
                current_date += timedelta(days=1)
                topic.save()

            if chapter.start_date != current_date:
                chapter.finish_date = current_date - timedelta(days=1)
            else:
                chapter.finish_date = current_date
            chapter.save()

        course.finish_date = current_date
        course.default_speaker = cleaned_data["default_speaker"]
        course.save()
        return super().form_valid(form)


class BecomeSpeakerView(MentorRequiredMixin, FormView):
    """View for set user as speaker for topic."""

    form_class = forms.TopicBecomeSpeakerForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        """Set user as speaker for Topic get by id from form field."""
        topic_id = form.cleaned_data["topic_id"]
        topic = get_object_or_404(models.Topic, id=topic_id)
        topic.speaker = self.request.user
        topic.save()
        return super().form_valid(form)


class RescheduleTopicView(MentorRequiredMixin, FormView):
    """View for change reading date for topic."""

    form_class = forms.RescheduleTopicForm
    success_url = reverse_lazy("homepage")

    def form_valid(self, form):
        """Set changed reading date to topic.

        Change finish date for topic chapter, start and finish dates
        all chapters below and all topics below the changed topic.

        Topic is ordered model, so all instance of topic have method next
        that return topic next in order. If order is finish it returns None.

        """
        cleaned_data = form.cleaned_data
        topic_id = cleaned_data["topic_id"]
        day_delta = cleaned_data["day_delta"]
        topic = get_object_or_404(models.Topic, id=topic_id)

        current_chapter = topic.chapter
        topic.reading_date += timedelta(days=day_delta)
        topic.save()

        # change dates for current chapter
        current_chapter.finish_date += timedelta(days=day_delta)
        current_topic = topic.next()
        while current_topic:
            current_topic.reading_date += timedelta(days=day_delta)
            current_topic.save()
            current_topic = current_topic.next()
        current_chapter.save()
        current_chapter = current_chapter.next()

        # change dates for all chapters below
        while current_chapter:
            current_chapter.start_date += timedelta(days=day_delta)
            current_chapter.finish_date += timedelta(days=day_delta)

            # change dates for all topics in the chapter
            current_topic = current_chapter.topics.first()
            while current_topic:
                current_topic.reading_date += timedelta(days=day_delta)
                current_topic.save()
                current_topic = current_topic.next()

            current_chapter.save()
            current_chapter = current_chapter.next()

        return super().form_valid(form)


class SolutionDetailView(DetailView, PermissionRequiredMixin, FormMixin, ):
    """Represent detail view for unique solution.

    Only mentors can view solution page. In this page mentor can check and
    evaluate user solution one time.
    """

    model = models.Solution
    template_name = "courses/solution.html"
    permission_required = (
        "courses.view_solution",
        "courses.create_evaluation",
    )
    form_class = forms.EvaluationForm

    def __init__(self, **kwargs):
        """Initialize self object."""
        super().__init__(**kwargs)
        self.object = None

    def get_context_data(self, **kwargs):
        """Add to context current user evaluation."""
        context = super().get_context_data(**kwargs)
        context["current_user_evaluation"] = self.object. \
            evaluated_solution.filter(
            owner=self.request.user
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        """Call form valid function and init form instance."""
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """Bound evaluation with current user and current solution."""
        evaluate_form_instance = form.save(commit=False)
        evaluate_form_instance.owner = self.request.user
        evaluate_form_instance.solution = self.object
        evaluate_form_instance.save()
        return HttpResponseRedirect(self.request.path)


class EvaluationUpdateForm(UpdateView):
    """Represent update view for unique evaluation."""
    model = models.Evaluation
    fields = [
        "mark",
        "comment",
    ]
    template_name = "courses/evaluation_update.html"

    def get_success_url(self):
        """Return a url of solution that has been evaluated for."""
        form_instance = self.get_form().instance
        solution_id = form_instance.solution_id
        return reverse_lazy("solution", kwargs={"pk": solution_id})


class DeleteEvaluateView(DeleteView, PermissionRequiredMixin):
    """Represent delete evaluation logic."""

    permission_required = ("courses.delete_solution",)
    model = models.Evaluation

    def get_success_url(self):
        """Return solution url of deleted evaluate."""
        return reverse_lazy(
            "solution",
            kwargs={"pk": self.get_object().solution.pk}
        )

    def get(self, *args, **kwargs):
        """Ignore the delete confirmation page."""
        return self.post(*args, **kwargs)
