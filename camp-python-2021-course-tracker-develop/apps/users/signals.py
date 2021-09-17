from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.core.files.storage import FileSystemStorage, default_storage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

import requests
from allauth.socialaccount.models import SocialAccount, SocialLogin
from allauth.socialaccount.signals import (
    pre_social_login,
    social_account_updated,
)

from apps.courses.models import Course
from apps.users.constants import DEFAULT_USER_PERMISSIONS
from apps.users.models import User

__all__ = (
    "add_new_user_to_group",
    "copy_default_avatar_to_media",
    "set_github_username_after_registration",
    "check_github_user_organization",
    "set_github_username",
)


# pylint: disable=unused-argument
@receiver(post_save, sender=User)
def add_new_user_to_group(sender: User, instance: User, **kwargs):
    """Add newly created user to default user group.

    Args:
        sender: User model class.
        instance: instance of class.
        **kwargs: any keyword arguments.
    """
    if instance.pk:
        default_group = Group.objects.get(
            name=DEFAULT_USER_PERMISSIONS["name"]
        )
        instance.groups.add(default_group)


@receiver(pre_save, sender=User)
def copy_default_avatar_to_media(sender: User, **kwargs):
    """Check exist default avatar in media root and add it there if not.

    If default media root doesn't have default avatar that this signal copy it
    from static files.

    Args:
        sender: User model class.
        **kwargs: any keyword arguments.

    """
    static_default_avatar_path = settings.STATICFILES_DIRS[0] / (
        "images/default_avatar/default.jpg"
    )
    media_default_avatar_path = FileSystemStorage().location + (
        "/users/default_avatar/default.jpg"
    )
    if not default_storage.exists(media_default_avatar_path):
        with open(static_default_avatar_path, "rb") as file:
            default_storage.save(media_default_avatar_path, ImageFile(
                file
            ))


@receiver(pre_save, sender=Course)
def copy_default_course_img_to_media(sender, **kwargs):
    """Check exist default course img in media root and add it there if not.

    If default media root doesn't have default course img
    that this signal copy it from static files.

    Args:
        sender: Course model class.
        **kwargs: any keyword arguments.

    """
    static_default_img_path = settings.STATICFILES_DIRS[0] / (
        "images/default_course_img/default.jpeg"
    )
    media_default_img_path = FileSystemStorage().location + (
        "/courses/default_course_img/default.jpeg"
    )
    if not default_storage.exists(media_default_img_path):
        with open(static_default_img_path, "rb") as file:
            default_storage.save(media_default_img_path, ImageFile(
                file
            ))


@receiver(post_save, sender=SocialAccount)
def set_github_username_after_registration(
    sender: SocialAccount,
    instance: SocialAccount,
    **kwargs
):
    """Add newly created user to default user group.

    Args:
        sender: User model class.
        instance: instance of class.
        **kwargs: any keyword arguments.

    Raises:
        ValidationError: if user already link with another github account.

    Todo: Add page for ValidationError which extends from base.html.
    """
    current_user = instance.user
    current_user.github_username = instance.extra_data["login"]
    current_user.is_active = True
    current_user.save()


@receiver(pre_social_login, sender=SocialLogin)
def check_github_user_organization(request, sociallogin, **kwargs):
    """Check if user who tries to connect his account is member of org.

    All allowed organizations are stored in
    apps.users.constants.ALLOWED_GITHUB_ORGANIZATIONS.

    Args:
        request: request object.
        sociallogin: SocialLogin object containing info about GH user.
        **kwargs: other keyword args.

    Raises:
        ValidationError: if status code is any other except 200 in all cases
            (user is not member of any organization).

    Todo: Add page for ValidationError which extends from base.html.
    """
    session = requests.Session()
    session.headers["Authorization"] = "Token " + sociallogin.token.token
    allowed_github_organizations = settings.ALLOWED_GITHUB_ORGANIZATIONS
    for org in allowed_github_organizations:
        membership_url = (
            f"https://api.github.com/orgs/{org}/memberships/"
            f"{sociallogin.account.extra_data['login']}"
        )

        response = session.get(membership_url)

        if response.status_code == 200:
            break
    else:
        raise ValidationError(_(
            "This user does not belong to any of allowed organizations or "
            "have no access to any of these organizations information."
        ))

    session.close()


@receiver(social_account_updated, sender=SocialLogin)
def set_github_username(request, sociallogin, **kwargs):
    """Set github username of account to actual GitHub username."""
    if not request.user.socialaccount_set.exists():
        raise ValidationError(_(
            "This user already have a github account."
        ))
    request.user.github_username = sociallogin.account.extra_data["login"]
    request.user.save()
