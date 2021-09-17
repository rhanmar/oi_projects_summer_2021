import uuid

import factory

from ..core.factories import SkillFactory
from .models import cvs, users


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generates test User instance."""

    avatar = factory.django.ImageField(color="magenta")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = users.User

    @factory.lazy_attribute
    def email(self):
        """Return formatted email."""
        return f"{uuid.uuid4()}@example.com"


class AdminUserFactory(UserFactory):
    """Factory for generates test User model with admin"s privileges."""

    class Meta:
        model = users.User

    is_superuser = True
    is_staff = True


class CVFactory(factory.django.DjangoModelFactory):
    """Factory for generate test CV instance."""

    class Meta:
        model = cvs.CV

    title = factory.Faker("company")
    description = factory.Faker("text")
    owner = factory.SubFactory(UserFactory)


class CVSkillEvaluationFactory(factory.django.DjangoModelFactory):
    """Factory for generate test bound between skill and cv."""

    class Meta:
        model = cvs.CVSkillEvaluation

    skill = factory.SubFactory(SkillFactory)
    cv_owner = factory.SubFactory(CVFactory)


class CVWith2SkillsFactory(CVFactory):
    """Factory for generate test CV instance with 2 skills."""

    membership1 = factory.RelatedFactory(
        CVSkillEvaluationFactory,
        factory_related_name="cv_owner"
    )
    membership2 = factory.RelatedFactory(
        CVSkillEvaluationFactory,
        factory_related_name="cv_owner"
    )
