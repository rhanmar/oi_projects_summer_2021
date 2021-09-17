from invoke import task

##############################################################################
# Data generation for database
##############################################################################


@task
def fill_sample_data(context, startups=None, vacancies=None):
    """Prepare sample data for local usage."""
    command = "python3 manage.py fill_sample_data"
    if startups:
        command += f" --startups={startups}"
    if vacancies:
        command += f" --vacancies={vacancies}"
    context.run(command)
