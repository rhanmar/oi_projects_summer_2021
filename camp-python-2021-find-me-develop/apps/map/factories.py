import random

from django.contrib.gis.geos import Point

import factory

from apps.dialogs.factories import DialogFactory
from apps.users.factories import UserFactory

from .models import Location, Meeting, MeetingReview


class LocationFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Location instance."""
    class Meta:
        model = Location

    title = factory.Faker("sentence")

    @factory.lazy_attribute
    def point(self):
        """Return random instance of Point."""
        random.seed()
        return Point(
            random.randint(15, 80),
            random.randint(15, 80),
        )


class MeetingFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Meeting instance."""
    class Meta:
        model = Meeting

    title = factory.Faker("sentence")
    created_by = factory.SubFactory(UserFactory)
    location = factory.SubFactory(LocationFactory)
    dialog = factory.SubFactory(DialogFactory)


class MeetingReviewFactory(factory.django.DjangoModelFactory):
    """Factory for generates test MeetingReview instance."""
    class Meta:
        model = MeetingReview

    title = factory.Faker("sentence")
    rate = factory.Faker(
        "pyint", min_value=1, max_value=5
    )
    created_by = factory.SubFactory(UserFactory)
    meeting = factory.SubFactory(MeetingFactory)
