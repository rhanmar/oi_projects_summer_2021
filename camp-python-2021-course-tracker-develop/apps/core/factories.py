from django.conf import settings

import factory
from allauth.socialaccount import models

from apps.core.models import ContentTypeModel


class TestContentTypeModel(ContentTypeModel):
    """Represent testing model for ContentTypeModel."""

    allowed_models = (
        "users.User",
        "courses.Course"
    )
    related_name = "testings"

    class Meta:
        app_label = "tests"
        db_table = "test_container"


class SocialAppFactory(factory.django.DjangoModelFactory):
    """Factory for social application."""

    class Meta:
        model = models.SocialApp

    provider = "github"
    name = "GH-test"
    client_id = settings.SOCIALACCOUNT_ID
    secret = settings.SOCIALACCOUNT_SECRET_KEY

    @factory.post_generation
    def sites_batch(self, create, extracted):
        """Add sites to social application."""
        if not create:
            return

        if extracted:
            for site in extracted:
                self.sites.add(site)
