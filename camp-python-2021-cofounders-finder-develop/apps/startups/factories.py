import random

from django.utils import timezone

import factory

from apps.startups import models
from apps.startups import statuses as text_choices
from apps.users.factories import UserFactory


def get_random_startup_status() -> str:
    """Return random status for Startup."""
    statuses = [value for value, _ in text_choices.StartupChoices.choices]
    return random.choice(statuses)


def get_random_vacancy_status() -> str:
    """Return random status for Vacancy."""
    statuses = [value for value, _ in text_choices.VacancyChoices.choices]
    return random.choice(statuses)


def get_random_request_status() -> str:
    """Return random status for Request."""
    statuses = [value for value, _ in text_choices.RequestChoices.choices]
    return random.choice(statuses)


class StartupFactory(factory.django.DjangoModelFactory):
    """Factory to create Startup instance."""

    class Meta:
        model = models.Startup

    title = factory.Faker("company")
    text = factory.Faker("text")
    owner = factory.SubFactory(UserFactory)
    end_date = timezone.now() + timezone.timedelta(weeks=7)
    status = factory.LazyFunction(get_random_startup_status)


class VacancyFactory(factory.django.DjangoModelFactory):
    """Factory to create Vacancy instance."""

    class Meta:
        model = models.Vacancy

    status = factory.LazyFunction(get_random_vacancy_status)
    title = factory.Faker("company")
    description = factory.Faker("text")
    startup = factory.SubFactory(StartupFactory)

    @factory.post_generation
    def skills(self, create, extracted, **kwargs):
        """Add skills to Vacancy."""
        if not create:
            return
        if extracted:
            for skill in extracted:
                self.skills.add(skill)


class RequestFactory(factory.django.DjangoModelFactory):
    """Factory to create Request instance."""

    vacancy = factory.SubFactory(VacancyFactory)
    message = factory.Faker("text")
    user = factory.SubFactory(UserFactory)
    status = factory.LazyFunction(get_random_request_status)

    class Meta:
        model = models.Request


class EmployeeFactory(factory.django.DjangoModelFactory):
    """Factory to create Employee instance."""

    vacancy = factory.SubFactory(VacancyFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Employee
