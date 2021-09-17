from django.urls import path

from apps.github.view import WebHookReceiverView

urlpatterns = [
    path(
        "webhooks/",
        WebHookReceiverView.as_view(),
        name="github_webhook",
    ),
]
