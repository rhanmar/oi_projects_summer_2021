from django.contrib.auth.views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.core.mixins import RedirectLoggedInUsersMixin
from apps.users.forms import (
    LogInForm,
    ResetPasswordConfirmForm,
    ResetPasswordForm,
    SignUpForm,
)
from apps.users.tasks import send_email_with_meetings_around_for_auth_user


class UserRegisterView(
    RedirectLoggedInUsersMixin,
    SuccessMessageMixin,
    CreateView
):
    """View for registration user."""

    template_name = "users/sign_up.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    success_message = "You have successfully registered!"


class UserLoginView(
    RedirectLoggedInUsersMixin,
    SuccessMessageMixin,
    LoginView
):
    """Log in view for User."""

    template_name = "users/login.html"
    form_class = LogInForm
    success_message = "You are successfully logged in!"

    def get_success_url(self):
        """Add Celery task to queue."""
        send_email_with_meetings_around_for_auth_user.delay(
            self.request.ipinfo.loc,
            self.request.ipinfo.city,
            self.request.user.id,
            self.request.user.email,
            self.request.user.first_name,
        )
        return super().get_success_url()


class UserPasswordResetView(RedirectLoggedInUsersMixin, PasswordResetView):
    """View for reset user password."""

    template_name = "users/reset_password.html"
    form_class = ResetPasswordForm
    email_template_name = "users/emails/password_reset.html"
    success_url = reverse_lazy("reset_password_done")
    extra_email_context = {
        "app_label": "FindMe",
        "app_url": reverse_lazy("main_page")
    }


class UserPasswordResetConfirmView(
    RedirectLoggedInUsersMixin,
    SuccessMessageMixin,
    PasswordResetConfirmView,
):
    """View for confirm password reset and change the password."""

    template_name = "users/reset_password_confirm.html"
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy("login")
    success_message = "Password changed successfully!"
