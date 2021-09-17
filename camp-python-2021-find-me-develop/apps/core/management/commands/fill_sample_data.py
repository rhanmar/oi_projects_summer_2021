from django.core.management import BaseCommand
from django.db import transaction

from apps.core.management.command_handlers.fill_sample_data_handler import (
    fill_sample_data_handler,
)


class Command(BaseCommand):
    """Command for filling data samples to database using factories.

    Write in console ``inv django.reset-and-fill-db`` to reset your db and fill
    with new data or ``inv django.add-sample-data`` to add new sample data
    without reset (or ``python3 manage.py fill_sample_data``).
    """

    num_users = 10

    @transaction.atomic
    def handle(self, *args, **options):
        """Fill db with sample data using factories."""

        fill_sample_data_handler(self.num_users)
