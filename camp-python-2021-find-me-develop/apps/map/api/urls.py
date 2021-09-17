from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("locations", views.LocationViewSet, basename="location")
router.register("meetings", views.MeetingViewSet, basename="meeting")
router.register("reviews", views.MeetingReviewViewSet, basename="review")

urlpatterns = router.urls
