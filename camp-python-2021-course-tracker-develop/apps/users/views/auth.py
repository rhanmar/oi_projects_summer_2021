from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, FormView, TemplateView

from libs.notifications.email import DefaultEmailNotification

from apps.users.forms import CustomPasswordResetForm, CustomUserCreationForm
from apps.users.models import User


class SignUpView(CreateView):
    """Implement user registration logic."""

    model = User
    form_class = CustomUserCreationForm
    template_name = "users/auth/signup.html"
    success_url = reverse_lazy("index")
    object = None

    def get_object(self, queryset=None):
        """Return current user as an object."""
        return self.request.user

    def post(self, request, *args, **kwargs):
        """Send an email if register is successful."""
        form = self.form_class(request.POST)

        if not form.is_valid():
            self.object = self.get_object()
            return self.form_invalid(form)

        new_user = form.save()
        mail_subject = _("Account activation")
        to_email = form.cleaned_data.get("email")

        site = Site.objects.get_current(request)
        domain = site.domain
        scheme = "https" if request.is_secure() else "http"
        app_url = f"{scheme}://{domain}"

        email_message = DefaultEmailNotification(
            subject=mail_subject,
            recipient_list=[to_email],
            template="users/emails/activate_account.html",
            uid=urlsafe_base64_encode(force_bytes(new_user.pk)),
            token=default_token_generator.make_token(new_user),
            app_url=app_url,
            app_label=settings.APP_LABEL,
        )

        try:
            email_message.send()
        except BadHeaderError:
            return HttpResponse(_("Invalid header found."))

        return render(
            request,
            "users/auth/activate_email_complete.html",
            {
                "text": "Message with confirmation link has been sent "
                        "to your email address. Please confirm your "
                        "email address to complete the registration.",
                "need_btn_login": False,
                "title": "Email has been sent",
            }
        )


@method_decorator(require_http_methods(["GET"]), name="dispatch")
class ActivateAccountView(TemplateView):
    """Activate account after email verification."""

    def get(self, request, *args, **kwargs):
        """Activate user if uid and token are valid."""
        uidb64 = self.kwargs.pop("uid64")
        token = self.kwargs.pop("token")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if not (user and default_token_generator.check_token(user, token)):
            return HttpResponse(_("Activation link is invalid!"))

        user.is_active = True
        user.save()
        return render(
            request,
            "users/auth/activate_email_complete.html",
            {
                "text": "Thank you for your registration. "
                        "Now you can login to your account.",
                "need_btn_login": True,
                "title": "Your account successfully activated",
            }
        )


class PasswordResetView(FormView):
    """Handle password reset request.

    Need custom one to override form_valid to call form's ``.save()`` method.
    """

    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password-reset-done")
    template_name = "users/auth/password_reset.html"

    def form_valid(self, form):
        """Save form and send email in form's ``save()`` method."""
        form.save()
        return super().form_valid(form)
