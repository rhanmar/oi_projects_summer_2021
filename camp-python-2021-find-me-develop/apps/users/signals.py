import os
import shutil

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.users.models import User


def get_default_avatar_static_path():
    """Returns user default avatar path from static."""
    static_default_avatar_path = (
        settings.STATICFILES_DIRS[0] / "images/default_avatar/"
    )
    return static_default_avatar_path


def get_default_avatar_media_path():
    """Returns user default avatar path from media."""
    media_default_avatar_path = settings.MEDIA_ROOT / "users/default_avatar/"
    return media_default_avatar_path


@receiver(pre_save, sender=User)
def copy_default_avatar_to_media(sender: User, **kwargs):
    """Check exist default avatar in media root and add it there if not.

    If default media root doesn't have default avatar that this signal copy it
    from static files.

    Args:
        sender: User model class.
        **kwargs: any keyword arguments.
    """
    # pylint: disable=unused-argument
    static_default_avatar_path = get_default_avatar_static_path()
    media_default_avatar_path = get_default_avatar_media_path()

    if not os.path.exists(media_default_avatar_path):
        shutil.copytree(static_default_avatar_path, media_default_avatar_path)


@receiver(post_save, sender=User)
def check_avatar(sender: User, instance: User, **kwargs):
    """Check if user avatar exists, else sets it to default."""
    # pylint: disable=unused-argument
    if not instance.avatar:
        media_default_avatar_path = get_default_avatar_media_path() / (
            "default_user_image.png"
        )
        relative_media_avatar_path = "/".join(
            media_default_avatar_path.parts[-3:]
        )

        instance.avatar = f"/{relative_media_avatar_path}"
        instance.save()
