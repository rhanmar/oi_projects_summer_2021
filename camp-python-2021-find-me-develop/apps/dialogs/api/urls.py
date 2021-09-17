from rest_framework.routers import DefaultRouter

from apps.dialogs.api.views import DialogMessageViewSet, DialogViewSet

router = DefaultRouter()
router.register(r"messages", DialogMessageViewSet, basename="messages")
router.register(r"", DialogViewSet, basename="dialogs")

urlpatterns = router.urls
