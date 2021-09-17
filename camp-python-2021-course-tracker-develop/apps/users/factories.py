import uuid

import factory

from .models import User

__all__ = (
    "UserFactory",
    "AdminUserFactory"
)


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generates test User instance."""
    is_active = True
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User

    @factory.lazy_attribute
    def email(self):
        """Return formatted email."""
        return f"{uuid.uuid4()}@saritasa.com"

    @factory.post_generation
    def add_group(self, create, extracted):
        """Add users to course."""
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class AdminUserFactory(UserFactory):
    """Factory for generates test User model with admin"s privileges."""

    class Meta:
        model = User

    @factory.post_generation
    def add_group(self, create, extracted):
        """Add users to course."""
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    is_superuser = True
    is_staff = True
