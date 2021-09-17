from datetime import datetime, timedelta

import pytz

from apps.map.factories import MeetingFactory
from apps.users.factories import ReviewFactory, UserFactory


def fill_sample_data_handler(num_users: int):
    """Fill database with sample data.

    Args:
        num_users: number of users to create.
        num_user_reviews: number of reviews to create for each user.
    """
    users = UserFactory.create_batch(num_users)

    for user in users:
        reviewers = users.copy()
        reviewers.remove(user)

        for reviewer in reviewers:
            ReviewFactory(
                reviewed=user,
                reviewer=reviewer,
            )

        MeetingFactory(
            created_by=user,
            deadline=datetime.now(tz=pytz.utc) + timedelta(days=1),
            max_people_limit=3,
        )
