from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.core.mixins import CheckBanBlacklistMixin, OwnerPermissionMixin
from apps.users.forms import UserReviewForm
from apps.users.models import Review, User


class UserAddReviewView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    SuccessMessageMixin,
    CreateView
):
    """View for add review for a user."""

    template_name = "users/user_add_edit_review.html"
    form_class = UserReviewForm
    success_url = reverse_lazy("user_profile")
    success_message = "New review was created successfully!"
    extra_context = {
        "title": "new review",
        "form_header": "New review",
        "submit_text": "Add",
    }

    def get_form_kwargs(self):
        """Add data about profile owner and request user to form's kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs["profile_owner_id"] = self.kwargs["user_id"]
        kwargs["request_user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Return custom context with reviewed fullname and page title."""
        context = super().get_context_data(**kwargs)
        reviewed_id = self.kwargs["user_id"]
        reviewed = User.objects.get(id=reviewed_id)
        context["reviewed"] = reviewed
        return context

    def form_valid(self, form):
        """Return new created instance of Review."""
        reviewer_id = self.request.user.id
        form.instance.reviewed_id = self.kwargs["user_id"]
        form.instance.reviewer_id = reviewer_id
        return super().form_valid(form)

    def get_success_url(self):
        """Return success redirect url to profile of reviewed user."""
        reviewed_id = self.kwargs["user_id"]
        return reverse("user_reviews", kwargs={"user_id": reviewed_id})


class UserReviewsView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    ListView
):
    """View for display all the user views."""

    template_name = "users/user_reviews.html"
    model = Review

    def get_queryset(self):
        """Return all reviews of user."""
        reviewed_id = self.kwargs["user_id"]
        return Review.objects.filter(reviewed_id=reviewed_id)

    def get_context_data(self, **kwargs):
        """Return custom context with visitor id."""
        context = super().get_context_data(**kwargs)
        reviewed_id = self.kwargs["user_id"]
        context["reviewed_user"] = User.objects.get(id=reviewed_id)
        return context


class UserEditReviewView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    OwnerPermissionMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """View for edit the review for user."""

    template_name = "users/user_add_edit_review.html"
    form_class = UserReviewForm
    owner_field_name = "reviewer_id"
    model = Review
    pk_url_kwarg = "review_id"
    extra_context = {
        "title": "edit review",
        "form_header": "Edit review",
        "submit_text": "Save",
    }
    success_message = "Review has been successfully modified!"

    def get_context_data(self, **kwargs):
        """Return custom context with reviewed fullname and page title."""
        context = super().get_context_data(**kwargs)
        reviewed_id = self.kwargs["user_id"]
        reviewed = User.objects.get(id=reviewed_id)
        context["reviewed_fullname"] = reviewed.get_fullname()
        context["reviewed"] = reviewed
        return context

    def get_success_url(self):
        """Return url after success update review."""
        reviewed_id = self.kwargs["user_id"]
        return reverse("user_reviews", kwargs={"user_id": reviewed_id})


class UserDetailReviewView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    DetailView
):
    """View for detail review of user."""

    template_name = "users/user_detail_review.html"
    model = Review
    pk_url_kwarg = "review_id"

    def get_context_data(self, **kwargs):
        """Return custom context with reviewed user."""
        context = super().get_context_data(**kwargs)
        reviewed_id = self.kwargs["user_id"]
        context["reviewed_user"] = User.objects.get(id=reviewed_id)
        return context


class UserDeleteReviewView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    OwnerPermissionMixin,
    SuccessMessageMixin,
    DeleteView
):
    """View for delete review of user."""

    model = Review
    owner_field_name = "reviewer_id"
    pk_url_kwarg = "review_id"
    success_message = "Review has been successfully deleted!"

    def get_success_url(self):
        """Return url after success delete review."""
        reviewed_id = self.kwargs["user_id"]
        return reverse(
            "user_profile",
            kwargs={"user_id": reviewed_id}
        )
