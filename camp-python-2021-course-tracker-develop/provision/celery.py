from invoke import task

from . import is_local_python
from .docker import up_containers


@task
def run(context, mode="info"):
    """Start celery worker"""
    if is_local_python:
        context.run(
            "celery --app config.celery:app worker --beat --scheduler=django "
            f"--loglevel={mode}"
        )
    else:
        up_containers(context, ["celery"])
