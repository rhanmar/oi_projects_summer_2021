import factory

from apps.skills.models import Skill


class SkillFactory(factory.django.DjangoModelFactory):
    """Factory to create Skill instance."""

    class Meta:
        model = Skill

    name = factory.Faker("name")
