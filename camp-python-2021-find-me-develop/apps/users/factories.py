import uuid

import factory

from .models import BlackList, Review, User, UserReport


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generates test User instance."""
    avatar = factory.django.ImageField(color="magenta")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self):
        """Return formatted email."""
        return f"{uuid.uuid4()}@example.com"


class AdminUserFactory(UserFactory):
    """Factory for generates test User model with admin"s privileges."""
    class Meta:
        model = User

    is_superuser = True
    is_staff = True


class ReviewFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Review instance."""
    class Meta:
        model = Review

    title = factory.Faker("sentence")
    rate = factory.Faker(
        "pyint", min_value=1, max_value=5
    )
    reviewer = factory.SubFactory(UserFactory)
    reviewed = factory.SubFactory(UserFactory)


class UserReportFactory(factory.django.DjangoModelFactory):
    """Factory for generates test UserReport instance."""
    class Meta:
        model = UserReport

    created_by = factory.SubFactory(UserFactory)
    reported = factory.SubFactory(UserFactory)


class BlackListFactory(factory.django.DjangoModelFactory):
    """Factory for generates test BlackList instance."""
    class Meta:
        model = BlackList

    user = factory.SubFactory(UserFactory)
    banned_user = factory.SubFactory(UserFactory)
