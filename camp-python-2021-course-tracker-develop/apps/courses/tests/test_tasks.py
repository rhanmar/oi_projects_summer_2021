from datetime import timedelta

from django.utils import timezone

import pytest

from apps.courses.constants import MAX_DAYS_FOR_BECOME_MENTOR
from apps.courses.models import Topic
from apps.courses.tasks import fill_topics_by_default_speakers

from .factories import create_filled_in_factory


@pytest.fixture
def not_planning_course():
    """Create course for tests."""
    return create_filled_in_factory()


@pytest.fixture
def course(not_planning_course):
    """Fill topics from created course."""
    now_date = timezone.now().date()
    topics = Topic.objects.filter(chapter__course=not_planning_course)
    for topic in topics:
        topic.reading_date = now_date
        topic.save()
        now_date += timedelta(days=1)
    return not_planning_course


def test_fill_topics_by_default_speakers(course):
    """Ensure was filled default speakers before reading_date.

    Check that all topics with reading_date smaller than 6 days
    was set default speaker of course. Other topics was not changed.

    For test was created greater than MAX_DAYS_FOR_BECOME_MENTOR
    topics which reading_date starts  from current date.
    So MAX_DAYS_FOR_BECOME_MENTOR + 1 topics from start
    should have default speaker.

    """
    fill_topics_by_default_speakers()
    topic_with_default_speaker = 0
    topics = Topic.objects.filter(chapter__course=course)

    for topic in topics:
        if topic.speaker == course.default_speaker:
            topic_with_default_speaker += 1

    count_topics = topics.count()
    assert count_topics != topic_with_default_speaker
    assert topic_with_default_speaker == MAX_DAYS_FOR_BECOME_MENTOR + 1
