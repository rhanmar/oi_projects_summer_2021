from rest_framework.routers import DefaultRouter

from . import views

# register URL like
# router.register(r"users", UsersAPIView)
router = DefaultRouter()
router.register(
    "users",
    views.UserInfoViewSet,
    basename="users"
)
router.register(
    "user_reviews",
    views.UserReviewViewSet,
    basename="user_reviews"
)

urlpatterns = router.urls
