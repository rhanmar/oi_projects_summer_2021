from django.core.exceptions import ValidationError

import pytest

from ..factories import ReviewFactory, UserFactory
from ..models import User


def test_unique_email_validation(user):
    """Test validation for case insensitive unique email."""
    new_user = User(email=user.email.upper(), password="1")
    with pytest.raises(ValidationError) as exc:
        new_user.full_clean()
    assert "email" in exc.value.error_dict


def test_get_average_rating_of_user(user):
    """Test get average rating of user."""
    ratings_of_user = [5.0, 2.0, 4.0, 1.0]
    avg_rating = sum(ratings_of_user) / len(ratings_of_user)
    for rating in ratings_of_user:
        ReviewFactory(reviewed=user, rate=rating)
    assert (
        User.objects
        .with_rating()
        .filter(id=user.id)
        .first()
        .rating == avg_rating
    )


def test_get_first_user_from_top():
    """Test get rating of user with max rating."""
    ratings_of_users = [[5.0, 2.0], [4.0, 1.0]]
    avg_ratings = [sum(ratings) / len(ratings) for ratings in ratings_of_users]
    max_rating = max(avg_ratings)
    for user_ratings in ratings_of_users:
        new_user = UserFactory()
        for rating in user_ratings:
            ReviewFactory(reviewed=new_user, rate=rating)
    top_user_rating = User.objects.get_top_users(10).first().rating
    assert top_user_rating == max_rating
