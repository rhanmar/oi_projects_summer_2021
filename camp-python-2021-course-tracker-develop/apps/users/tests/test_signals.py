from django.contrib.auth.models import Group

from apps.users.constants import DEFAULT_USER_PERMISSIONS


def test_add_new_user_to_group_works_correct(user):
    """Ensure that add_new_user_to_group signal add user to default group."""
    default_group = Group.objects.get(name=DEFAULT_USER_PERMISSIONS["name"])
    assert default_group in user.groups.all()
