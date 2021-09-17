from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, TemplateView

from libs.notifications.email import DefaultEmailNotification

from apps.users.forms import EmailUserForm
from apps.users.models import User


class SignUpView(CreateView):
    """Implement user registration logic."""
    model = User
    form_class = EmailUserForm
    template_name = "users/registration/signup.html"
    success_url = reverse_lazy("index")

    def __init__(self, **kwargs):
        """Init self object of class."""
        super().__init__(**kwargs)
        self.object = None

    def get_object(self, queryset=None):
        """Return current user as an object."""
        return self.request.user

    def post(self, request, *args, **kwargs):
        """Send an email if registration is successful."""
        form = self.form_class(request.POST)

        if not form.is_valid():
            self.object = self.get_object()
            return self.form_invalid(form)

        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        mail_subject = _("Account activation")
        to_email = form.cleaned_data.get("email")

        confirmation_lazy = reverse_lazy(
            "activate-account",
            kwargs={
                "uid64": urlsafe_base64_encode(force_bytes(new_user.pk)),
                "token": default_token_generator.make_token(new_user),
            }
        )
        confirmation_url = request.build_absolute_uri(confirmation_lazy)

        email_message = DefaultEmailNotification(
            subject=mail_subject,
            recipient_list=[to_email],
            template="users/emails/account_activation_email.html",
            confirmation_url=confirmation_url,
        )

        try:
            email_message.send()
        except BadHeaderError:
            return HttpResponseRedirect(reverse_lazy(
                "activate_account_invalid",
            ))

        return HttpResponseRedirect(reverse_lazy(
            "activate_account_done",
        ))


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
        return HttpResponseRedirect(reverse_lazy(
            "activate_account_complete",
        ))


class ActivateAccountCompleteView(TemplateView):
    """View which render a signup complete information."""

    template_name = "users/registration/signup_complete.html"


class ActivateAccountDoneView(TemplateView):
    """View which render a signup done information."""

    template_name = "users/registration/signup_done.html"


class ActivateAccountInvalidView(TemplateView):
    """View which render a signup invalid information."""

    template_name = "users/registration/signup_invalid.html"
