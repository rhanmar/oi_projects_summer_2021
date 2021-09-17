from invoke import task

##############################################################################
# Data generation for database
##############################################################################


@task
def fill_sample_data(context):
    """Prepare sample data for local usage."""
    raise NotImplementedError("Implement sample data generation")
