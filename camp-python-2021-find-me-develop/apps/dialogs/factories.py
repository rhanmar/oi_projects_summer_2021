import factory

from apps.users.factories import UserFactory

from .models import Attachment, Dialog, DialogMember, Message


class DialogFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Dialog instance."""
    class Meta:
        model = Dialog

    title = factory.Faker("sentence")


class DialogMemberFactory(factory.django.DjangoModelFactory):
    """Factory for generates test DialogMember instance."""
    class Meta:
        model = DialogMember

    dialog = factory.SubFactory(DialogFactory)
    member = factory.SubFactory(UserFactory)


class MessageFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Message instance."""
    class Meta:
        model = Message

    text = factory.Faker("text")
    sender = factory.SubFactory(UserFactory)
    dialog = factory.SubFactory(DialogFactory)


class AttachmentFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Attachment instance."""
    class Meta:
        model = Attachment

    file = factory.django.FileField(color="blueviolet")
    message = factory.SubFactory(MessageFactory)
