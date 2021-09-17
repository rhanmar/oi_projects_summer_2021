from invoke import task

##############################################################################
# Data generation for database
##############################################################################


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    command = "python3 manage.py fill_sample_data"
    context.run(command)
