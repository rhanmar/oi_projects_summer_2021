from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.core.mixins import CheckBanBlacklistMixin, CheckBanMixin
from apps.users.forms import UserBlacklistForm, UserEditForm
from apps.users.models import BlackList, User


class UserProfileView(
    LoginRequiredMixin,
    CheckBanBlacklistMixin,
    TemplateView
):
    """View for user profile."""

    template_name = "users/user_profile.html"

    def get_context_data(self, **kwargs):
        """Add extra data to context.

        Add to context user, is_self_profile, user rating
        and is_in_profile_blacklist.
        If is_in_blacklist is True, also add blacklist_item_id.

        """
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs["user_id"]
        user = User.objects.with_rating().get(id=profile_id)
        context["user"] = user
        is_self_profile = self.request.user.id == profile_id
        context["is_self_profile"] = is_self_profile
        if not is_self_profile:
            is_already_reported = user.reports_to.filter(
                    created_by_id=self.request.user.id,
                ).exists()
            context["is_already_reported"] = is_already_reported

            is_in_blacklist = False
            blacklist_item = self.request.user.banned.filter(
                banned_user_id=user.id
            ).first()
            if blacklist_item:
                is_in_blacklist = True
                context["blacklist_item_id"] = blacklist_item.id
            context["is_in_blacklist"] = is_in_blacklist

            review = self.request.user.reviews.filter(
                reviewed_id=user.id
            )
            is_reviewed_by_current_user = review.exists()
            context["is_reviewed"] = is_reviewed_by_current_user
            if is_reviewed_by_current_user:
                context["review"] = review.first()

        return context


class UserEditProfileView(
    LoginRequiredMixin,
    CheckBanMixin,
    SuccessMessageMixin,
    UpdateView
):
    """View for edit user info."""

    template_name = "users/user_edit.html"
    form_class = UserEditForm
    success_message = "Profile was edited successfully!"

    def get_object(self, queryset=None):
        """Return object that will be edited."""
        return self.request.user

    def get_success_url(self):
        """Return success redirect url to user profile with edited info."""
        user_id = self.request.user.id
        return reverse("user_profile", kwargs={"user_id": user_id})

    def get_context_data(self, **kwargs):
        """Add to context info about user's avatar."""
        context = super().get_context_data(**kwargs)
        has_avatar = True
        try:
            hasattr(self.request.user.avatar, "url")
        except ValueError:
            has_avatar = False
        context["has_avatar"] = has_avatar
        return context


class BannedUserView(
    LoginRequiredMixin,
    TemplateView
):
    """Show message to banned user."""

    template_name = "users/ban_page.html"


class UserAddToBlacklistView(
    LoginRequiredMixin,
    CheckBanMixin,
    CreateView
):
    """View for adding user to BlackList."""

    model = BlackList
    template_name = "users/blacklist_add_user.html"
    pk_url_kwarg = "user_id"
    form_class = UserBlacklistForm

    def __init__(self, **kwargs):
        """Initialize self object."""
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        """Check that visitor doesn't add himself to blacklist."""
        profile_owner_id = self.kwargs["user_id"]
        if profile_owner_id == request.user.id:
            return HttpResponseForbidden(
                "You can't add yourself to BlackList."
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle POST request.

        This handler creates blacklist instance and redirect to
        current user's blacklist.

        If there is no chosen for adding user in DB or
        this user is already in the blacklist,
        exception is raised.

        """
        try:
            user_to_add = get_object_or_404(
                User,
                pk=kwargs["user_id"]
            )
        except Http404:
            return HttpResponseForbidden(
                "No such user."
            )
        try:
            BlackList.objects.create(
                user=request.user,
                banned_user=user_to_add
            )
        except IntegrityError:
            return HttpResponseForbidden(
                "You have already added this user to your Blacklist."
            )
        return HttpResponseRedirect(reverse("user_blacklist"))


class UserBlacklistView(LoginRequiredMixin, CheckBanMixin, ListView):
    """View for showing current user's blacklist."""

    template_name = "users/blacklist_list.html"
    context_object_name = "blacklist"

    def get_queryset(self):
        """Return current user's blacklist."""
        return self.request.user.banned.select_related(
            "user", "banned_user"
        ).all()


class UserRemoveFromBlacklistView(
    LoginRequiredMixin,
    CheckBanMixin,
    DeleteView
):
    """View for removing user from current user's blacklist."""

    model = BlackList
    success_url = reverse_lazy("user_blacklist")
    pk_url_kwarg = "bl_item_id"
    template_name = "users/blacklist_remove_user.html"
