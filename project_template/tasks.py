from invoke import Collection

from provision import (
    celery,
    data,
    django,
    docker,
    git,
    linters,
    open_api,
    project,
    tests,
    k8s,
)

ns = Collection(
    celery,
    django,
    docker,
    data,
    linters,
    project,
    tests,
    git,
    open_api,
    k8s,
)

# Configurations for run command
ns.configure({'run': {'pty': True, 'echo': True}})
