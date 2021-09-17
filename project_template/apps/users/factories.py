import uuid

import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generates test User instance."""
    avatar = factory.django.ImageField(color="magenta")

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
