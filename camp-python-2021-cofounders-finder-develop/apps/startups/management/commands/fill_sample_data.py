from random import randint

from django.core.management.base import BaseCommand

from apps.startups import factories


class Command(BaseCommand):
    """Command for filling data samples to database using factories.

    Optional args:
        startups (int): default 5,
        vacancies (int): default 3.
    """

    help = "Fills database with data samples"
    startups = 5
    vacancies = 3

    def add_arguments(self, parser):
        """Add optional args `--startups` and `--vacancies` to command."""
        parser.add_argument(
            "--startups",
            type=int,
            default=self.startups
        )
        parser.add_argument(
            "--vacancies",
            type=int,
            default=self.vacancies
        )

    def handle(self, *args, **options):
        """Save factory instances to DB."""

        startups = options["startups"]
        vacancies = options["vacancies"]

        for _ in range(startups):
            startup = factories.StartupFactory()
            for _ in range(vacancies):
                vacancy = factories.VacancyFactory(startup=startup)
                factories.EmployeeFactory(vacancy=vacancy)
                factories.RequestFactory.create_batch(
                    vacancy=vacancy,
                    size=randint(0, 2)  # Creates random `size` in range [0, 2]
                )

        self.stdout.write(
            self.style.SUCCESS("Data samples were successfully filled!")
        )
