from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.http import HttpResponseRedirect
from django.urls import resolve


class LoginRequiredMiddleware(AuthenticationMiddleware):
    """Applies login required permission to entire project.

    Define urls in `LOGIN_EXEMPT_VIEWS` to be exempted.
    """

    def __call__(self, request):
        """Code to be executed for each request before the view are called."""
        available_settings = dir(settings)
        if "LOGIN_URL" not in available_settings:
            raise Exception("LOGIN_URL must be defined at settings.")
        if "LOGIN_EXEMPT_VIEWS" not in available_settings:
            raise Exception("LOGIN_EXEMPT_VIEWS must be defined at settings.")
        login_url = settings.LOGIN_URL

        login_exempt_views = settings.LOGIN_EXEMPT_VIEWS
        view_name = resolve(request.path).view_name

        # No need to process URLs if user already logged in
        if request.user.is_authenticated or view_name in login_exempt_views:
            return self.get_response(request)
        # Direct to login URL is user is not authenticated
        return HttpResponseRedirect(login_url)
