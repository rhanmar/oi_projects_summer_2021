from datetime import date, datetime, timedelta

from django.utils import timezone

import factory

from apps.courses import models
from apps.users.factories import AdminUserFactory, UserFactory


class CourseFactory(factory.django.DjangoModelFactory):
    """Create new Course instance."""

    title = factory.Faker("name")
    description = factory.Faker("text")
    is_hidden = False
    start_date = date.today()
    finish_date = date.today() + timedelta(weeks=7)
    default_speaker = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Course

    @factory.post_generation
    def create_users(self, create, extracted):
        """Add users to course."""
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class ChapterFactory(factory.django.DjangoModelFactory):
    """Factory of courses.Chapter model."""

    course = factory.SubFactory(CourseFactory)
    title = factory.Faker("name")
    description = factory.Faker("text")
    start_date = date.today()
    finish_date = date.today() + timedelta(weeks=7)

    class Meta:
        model = models.Chapter


class TopicFactory(factory.django.DjangoModelFactory):
    """Factory of courses.Topic model."""

    chapter = factory.SubFactory(ChapterFactory)
    title = factory.Faker("name")
    description = factory.Faker("text")
    reading_date = timezone.now()

    class Meta:
        model = models.Topic


class TaskFactory(factory.django.DjangoModelFactory):
    """Factory of courses.Task model."""

    topic = factory.SubFactory(TopicFactory)
    title = factory.Faker("name")
    description = factory.Faker("text")

    class Meta:
        model = models.Task


class SolutionFactory(factory.django.DjangoModelFactory):
    """Factory of courses.Solution model."""

    class Meta:
        model = models.Solution

    owner = factory.SubFactory(UserFactory)
    task = factory.SubFactory(TaskFactory)
    solution_description = factory.Faker("text")


def create_filled_in_factory():
    """Create filled course.

    Course have:
        8 students;
        2 mentors;
        5 chapters;
        25 topics;
        100 tasks.
    """
    users = UserFactory.create_batch(8, add_group=(2, ))
    mentors = AdminUserFactory.create_batch(2, add_group=(3, ))
    users.extend(mentors)
    course = CourseFactory.create(
        create_users=users,
        default_speaker=mentors[0],
    )
    chapters = ChapterFactory.create_batch(5, course=course)

    for chapter in chapters:
        topics = TopicFactory.create_batch(
            5,
            chapter=chapter,
            speaker=mentors[0],
            reading_date=datetime.today() - timedelta(days=1),
        )
        for topic in topics:
            TaskFactory.create_batch(4, topic=topic)
    return course
