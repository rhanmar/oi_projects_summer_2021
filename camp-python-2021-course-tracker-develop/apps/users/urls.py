from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls import include, path, reverse_lazy
from django.utils.translation import gettext_lazy as _

from allauth.socialaccount import views

from apps.users.views import (
    ActivateAccountView,
    MentorsView,
    PasswordResetView,
    SignUpView,
    UserDetailView,
    UserProfileUpdateView,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            redirect_authenticated_user=True,
            template_name="users/auth/login.html",
        ),
        name="login"
    ),
    path(
        "signup/",
        SignUpView.as_view(),
        name="signup",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            next_page=reverse_lazy("homepage")
        ),
        name="logout",
    ),
    path(
        "signup/<uid64>/<token>/",
        ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/done/",
        PasswordResetDoneView.as_view(
            template_name="users/auth/password_reset_done.html",
            title=_("Password reset sent"),
        ),
        name="password-reset-done",
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("password-reset-complete"),
            template_name="users/auth/password_reset_confirm.html",
        ),
        name="password-reset-confirm",
    ),
    path(
        "password/reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/auth/password_reset_complete.html",
            title=_("Reset complete"),
        ),
        name="password-reset-complete",
    ),
    path(
        "profile/update/",
        UserProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "mentors/",
        MentorsView.as_view(),
        name="mentors",
    ),
    path(
        "<int:pk>/",
        UserDetailView.as_view(),
        name="user",
    ),
    path("", include("allauth.urls")),
    path(
        "social/connections/",
        views.ConnectionsView.as_view(success_url=reverse_lazy("homepage")),
        name="socialaccount_connections",
    ),
]
