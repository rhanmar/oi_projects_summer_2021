from django.urls import path

from .views import DialogDetailView

urlpatterns = [
    path(
        "dialog/<int:dialog_id>/",
        DialogDetailView.as_view(),
        name="dialog_detail"
    )
]
