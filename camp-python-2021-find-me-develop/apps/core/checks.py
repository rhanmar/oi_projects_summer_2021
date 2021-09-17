from apps.users.models import BlackList, User


def check_is_banned(*args, **kwargs):
    """Check that current user is banned."""
    request = args[0]
    return request.user.is_banned


def check_is_in_blacklist(*args, **kwargs):
    """Check that current user is in profile owner's blacklist."""
    request = args[0]
    profile_owner = User.objects.get(pk=kwargs["user_id"])
    who_banned_current_user_ids = request.user.banned_by.all(
        ).values_list("user_id", flat=True)
    return profile_owner.id in who_banned_current_user_ids


def check_does_not_user_exist(*args, **kwargs):
    """Check that user_id from URL is in DB."""
    if kwargs.get("user_id") is None:
        return False
    return not User.objects.filter(pk=kwargs["user_id"]).exists()


def check_does_not_blacklist_item_exist(*args, **kwargs):
    """Check that bl_item_id from URL is in DB."""
    if kwargs.get("bl_item_id") is None:
        return False
    return not BlackList.objects.filter(pk=kwargs["bl_item_id"]).exists()
