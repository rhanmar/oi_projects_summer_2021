from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import BaseCommand

from allauth.socialaccount import models

from apps.core.factories import SocialAppFactory
from apps.courses.tests import factories as course_factory


class Command(BaseCommand):
    """Command for filling data samples to database using factories.

    Write in console 'inv data.fill-sample-data' or
    'python3 manage.py fill_sample_data' and your db fill up with sample data.
    Also add social github account account to db if it doesn't exists.
    """

    def handle(self, *args, **options):
        """Save factory instances to DB."""

        course_factory.create_filled_in_factory()

        if not models.SocialApp.objects.exists():
            site = Site.objects.get_or_create()[0]
            site.domain = settings.FRONTEND_URL
            site.name = "Current site"
            site.save()
            SocialAppFactory.create(sites_batch=(site,))

        self.stdout.write(
            self.style.SUCCESS("Data samples were successfully filled!")
        )
