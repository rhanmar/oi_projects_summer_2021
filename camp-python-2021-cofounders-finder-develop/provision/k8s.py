##############################################################################
# Shortcuts for k8s
##############################################################################
from invoke import task

from . import common

NAMESPACE = "camp-python"
APP = "cofounders-finder"


def _get_pod_cmd(component: str) -> str:
    """Get command for getting exact pod."""
    return (
        f"kubectl get pods "
        f"-l app.kubernetes.io/component={component},app={APP} "
        f"--no-headers -o=\"custom-columns=NAME:.metadata.name\""
    )


@task
def login(context):
    """Login into k8s via teleport."""
    common.success("Login into kubernetes CI")
    context.run("tsh login --proxy=teleport.saritasa.rocks:443 --auth=github")


@task
def set_context(context):
    """Set k8s context to current project."""
    common.success("Setting context for k8s")
    context.run(
        f"kubectl config set-context --current --namespace={NAMESPACE}"
    )


@task
def logs(context, component="backend"):
    """Get logs for k8s pod."""
    set_context(context)
    common.success(f"Getting logs from {component}")
    context.run(f"kubectl logs $({_get_pod_cmd(component)})")


@task
def pods(context):
    """Get pods from k8s."""
    set_context(context)
    common.success("Getting pods")
    context.run("kubectl get pods")


@task
def execute(
    context,
    entry="/cnb/lifecycle/launcher bash",
    component="backend"
):
    """Execute command inside of k8s pod."""
    set_context(context)
    common.success(f"Entering into {component} with {entry}")
    context.run(f"kubectl exec -ti $({_get_pod_cmd(component)}) -- {entry}")


@task
def python_shell(context, component="backend"):
    """Enter into python shell."""
    execute(context, component=component, entry="shell_plus")
