import os

from invoke import task

from . import common, data, django, docker, git, is_local_python, tests

##############################################################################
# Build project locally
##############################################################################


def copylocal(context, force_update=True):
    """Copy local settings from template

    Args:
        force_update(bool): rewrite file if exists or not
    """
    local_settings = "config/settings/local.py"
    local_template = "config/settings/local.template.py"

    if force_update or not os.path.isfile(local_settings):
        context.run(
            " ".join(["cp", local_template, local_settings])
        )


@task
def build(context):
    """Build python environ"""
    if is_local_python:
        install_requirements(context)
    else:
        common.success("Rebuilding docker infra")
        cmd = "docker-compose build"
        context.run(cmd)


@task
def init(context, clean=False):
    """Prepare env for working with project."""
    common.success("Setting up git config")
    git.hooks(context)
    git.gitmessage(context)
    common.success("Initial assembly of all dependencies")
    install_tools(context)
    if clean:
        docker.clear(context)
    copylocal(context)
    build(context)
    django.migrate(context)
    tests.run(context)
    django.createsuperuser(context)
    # if this is first start of the project
    # then the following line will generate exception
    # informing first developer to make factories
    try:
        data.fill_sample_data(context)
    except NotImplementedError:
        common.warn(
            "Awesome, almost everything is Done! \n"
            "You're the first developer - pls generate factories \n"
            "for test data and setup development environment"
        )


##############################################################################
# Manage dependencies
##############################################################################
@task
def install_tools(context):
    """Install shell/cli dependencies, and tools needed to install requirements

    Define your dependencies here, for example
    local("sudo npm -g install ngrok")
    """
    context.run("pip install --upgrade setuptools pip pip-tools wheel")


@task
def install_requirements(context, env="development"):
    """Install local development requirements"""
    common.success(
        "Install requirements with pip from {env}.txt".format(env=env)
    )
    context.run("pip install -r requirements/{env}.txt".format(env=env))


@task
def pip_compile(context, update=False):
    """Compile requirements with pip-compile"""
    common.success("Compile requirements with pip-compile")
    upgrade = "-U" if update else ""
    in_files = [
        "requirements/production.in",
        "requirements/development.in",
    ]
    for in_file in in_files:
        context.run(
            "pip-compile -q {in_file} {upgrade}".format(
                in_file=in_file,
                upgrade=upgrade),
        )


@task
def pip_compile_and_rebuild(context, update=False):
    """Compile requirements with pip-compile and perform rebuild."""
    pip_compile(context, update)
    build(context)
