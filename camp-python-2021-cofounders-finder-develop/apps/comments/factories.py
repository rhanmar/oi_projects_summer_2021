import factory

from apps.comments import models
from apps.startups.factories import StartupFactory
from apps.users.factories import UserFactory


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory to create Comment instance without parent comment."""

    class Meta:
        model = models.Comment

    title = factory.Faker("company")
    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    startup = factory.SubFactory(StartupFactory)


class CommentFactoryWithParentComment(factory.django.DjangoModelFactory):
    """Factory to create Comment instance with parent comment."""

    class Meta:
        model = models.Comment

    title = factory.Faker("company")
    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
    parent_comment = factory.SubFactory(CommentFactory)
    startup = factory.SubFactory(StartupFactory)
