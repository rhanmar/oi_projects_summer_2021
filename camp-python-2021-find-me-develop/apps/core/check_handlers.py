from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from apps.users.models import User


def handle_is_banned(*args, **kwargs):
    """Handle error from 'check_is_banned'."""
    return HttpResponseRedirect(
        reverse("ban_page")
    )


def handle_is_in_blacklist(*args, **kwargs):
    """Handle error from 'check_is_in_blacklist'."""
    request = args[0]
    profile_owner = User.objects.get(pk=kwargs["user_id"])
    is_profile_banned_by_current_user = False
    who_current_user_banned = request.user.banned.all(
        ).values_list("banned_user_id", flat=True)
    if profile_owner.id in who_current_user_banned:
        is_profile_banned_by_current_user = True
    return render(
        request,
        "users/blacklist_message.html",
        {
            "profile_owner_id": profile_owner.id,
            "is_profile_in_bl": is_profile_banned_by_current_user,
        }
    )


def handle_does_not_user_exist(*args, **kwargs):
    """Handle error from 'check_does_not_user_exist'."""
    return HttpResponseForbidden(
        "No such user."
    )


def handle_does_not_blacklist_item_exist(*args, **kwargs):
    """Handle error from 'check_does_not_blacklist_item_exist'."""
    return HttpResponseForbidden(
        "Not valid"
    )
