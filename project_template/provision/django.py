##############################################################################
# Django commands and stuff
##############################################################################
from invoke import Responder, task

from . import common, start, system


@task
def manage(context, command, watchers=()):
    """Run ``manage.py`` command.

    docker-compose run --rm web python3 manage.py <command>

    Args:
        context: Invoke context
        command: Manage command
        watchers: Automated responders to command

    """
    return start.run_python(
        context,
        " ".join(["manage.py", command]),
        watchers=watchers,
    )


@task
def makemigrations(context):
    """Run makemigrations command and chown created migrations."""
    common.success("Django: Make migrations")
    manage(context, "makemigrations")
    if not start.is_local_python:
        system.chown(context)


@task
def check_new_migrations(context):
    """Check if there is new migrations or not."""
    common.success("Checking migrations")
    manage(context, "makemigrations --check --dry-run")


@task
def migrate(context):
    """Run ``migrate`` command."""
    common.success("Django: Apply migrations")
    manage(context, "migrate")


@task
def resetdb(context):
    """Reset database to initial state (including test DB)."""
    common.success("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    makemigrations(context)
    migrate(context)
    createsuperuser(context)


@task
def createsuperuser(
    context,
    email="root@root.com",
    username="root",
    password="root",
):
    """Create superuser."""
    common.success("Create superuser")
    responder_email = Responder(
        pattern=r"Email address: ",
        response=email + "\n",
    )
    responder_user_name = Responder(
        pattern=r"Username: ",
        response=username + "\n",
    )
    responder_password = Responder(
        pattern=r"(Password: )|(Password \(again\): )",
        response=password + "\n",
    )
    manage(
        context,
        command="createsuperuser",
        watchers=[
            responder_email,
            responder_user_name,
            responder_password,
        ]
    )


@task
def run(context):
    """Run development web-server."""

    # start dependencies (so even in local mode this command
    # is working successfully
    # if you need more default services to be started define them
    # below, like celery, etc.
    common.success("Running web app")
    manage(
        context,
        "runserver_plus 0.0.0.0:8000  --reloader-type stat",
    )


@task
def shell(context, params=None):
    """Shortcut for manage.py shell_plus command.

    Additional params available here:
        https://django-extensions.readthedocs.io/en/latest/shell_plus.html
    """
    common.success("Entering Django Shell")
    manage(context, "shell_plus --ipython {}".format(params or ""))


@task
def dbshell(context):
    """Open postgresql shell with credentials from either local or dev env."""
    common.success("Entering DB shell")
    manage(context, "dbshell")
