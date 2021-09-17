from collections import namedtuple

from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.core.check_handlers import (
    handle_does_not_blacklist_item_exist,
    handle_does_not_user_exist,
    handle_is_banned,
    handle_is_in_blacklist,
)
from apps.core.checks import (
    check_does_not_blacklist_item_exist,
    check_does_not_user_exist,
    check_is_banned,
    check_is_in_blacklist,
)

CheckHandlerMap = namedtuple("CheckHandlerMap", ["check", "handler"])


class RedirectLoggedInUsersMixin:
    """Class that redirects active users to the redirect url or do nothing.

    Attrs:
        redirect_url(str): redirect url for authenticated users.

    """

    redirect_url = reverse_lazy("main_page")

    def dispatch(self, request, *args, **kwargs):
        """Redirect active users to the redirect url for active users."""
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)


class OwnerPermissionMixin(AccessMixin):
    """Mixin checks object owner makes request for delete.

    Expects:
        self.get_object(queryset=None)

    Attrs:
        owner_field_name(str): attr name where stored owner.

    """

    owner_field_name = "created_by_id"

    def dispatch(self, request, *args, **kwargs):
        """Return Forbidden if user is not object owner or call dispatch."""
        # pylint: disable=no-member
        obj = self.get_object()
        if not hasattr(obj, self.owner_field_name):
            raise AttributeError(
                "Invalid name of owner field of object: "
                f"{self.owner_field_name}"
            )

        owner_id = request.user.id
        if getattr(obj, self.owner_field_name) != owner_id:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class BaseChecksMixin(UserPassesTestMixin):
    """Base view for all checks.

    There is a list of check functions in 'base_checks_and_handlers'
    and checks from child mixins in 'checks_and_handlers'.

    """

    base_checks_and_handlers = {
        CheckHandlerMap(
            check=check_does_not_user_exist,
            handler=handle_does_not_user_exist
        ),
        CheckHandlerMap(
            check=check_does_not_blacklist_item_exist,
            handler=handle_does_not_blacklist_item_exist
        ),
    }
    checks_and_handlers = {}

    def test_func(self):
        """Do all checks.

        At the start this function unites base checks and checks from
        child mixins.
        Then it iterates over the list of checks, calls it and, if
        check is failed, add the check in kwargs and returns False.
        If all checks are passed it returns True.

        When it returns False, 'dispatch' from UserPassesTestMixin
        calls 'handle_no_permission'.

        """
        self.checks_and_handlers = (
            list(self.base_checks_and_handlers)
            + list(self.checks_and_handlers)
        )

        for item in self.checks_and_handlers:
            if_check_falls = item.check(self.request, **self.kwargs)
            if if_check_falls:
                self.kwargs["failed_check"] = item
                return False
        return True

    def handle_no_permission(self):
        """Call handler when check is failed.

        Also there is a 'is_authenticated' check because of LoginRequiredMixin.
        """
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        failed_check = self.kwargs["failed_check"]
        return failed_check.handler(self.request, **self.kwargs)


class CheckBanBlacklistMixin(BaseChecksMixin):
    """Verify the current user isn't banned and not in profile blacklist.

    This view add extra data to 'checks_and_handlers' in BaseCheckMixin.
    The data contains check functions and it's handler.

    """

    checks_and_handlers = {
        CheckHandlerMap(
            check=check_is_banned,
            handler=handle_is_banned
        ),
        CheckHandlerMap(
            check=check_is_in_blacklist,
            handler=handle_is_in_blacklist
        ),
    }


class CheckBanMixin(BaseChecksMixin):
    """Verify that the current user is not banned.

    This view add extra data to 'checks_and_handlers' in BaseCheckMixin.
    The data contains check functions and it's handler.

    """

    checks_and_handlers = {
        CheckHandlerMap(
            check=check_is_banned,
            handler=handle_is_banned
        ),
    }
